from RSAkeys import *
import time


################################################################################################################

# Returns the partial quotients for rational fraction
def getPartialQuot(u, v):
    
    a = u//v

    quot = [a]
    while (a*v!=u):
        temp = u - a*v
        u = v
        v = temp
        a = u//v
        quot.append(u//v)
    return quot

################################################################################################################

# Function to convert continued fraction to rational fraction
def getRational(fraction):
     
    if len(fraction) is 0:
        return (0,1)

    denominator = 1
    numerator = fraction[-1]

    for i in range(2,len(fraction)+1):
        temp = fraction[-i] * numerator + denominator
        denominator = numerator
        numerator = temp

    return (numerator,denominator)

################################################################################################################

# Function to calculate estimates from partial quotients list
def getEstimates(fraction):
     
    estimates = [(0,0) for _ in range(len(fraction))]

    for i in range(len(fraction)):
        temp = [0 for _ in range(i)]
        if (i%2==0):
            temp[0:i] = fraction[0:i]
        else:
            temp[0:i-1] = (fraction[0:i-1])
            temp[i-1] = fraction[i-1]+1

        estimates[i] = (getRational(temp))
        
    return estimates

################################################################################################################

# Function to actually calculate d knowing (N,e)
def crackRSA(N, e):
   
    fraction = getPartialQuot(e, N)
    estimates = getEstimates(fraction)
    
    for (g,d) in estimates:
        
        # Check if d is correct
        if (g != 0) and ((e*d-1)%g == 0):

            totient = (e*d-1)//g                                #Calculates (p-1)(q-1)
            s = N - totient + 1
            
            # Check the determinant of x^2 - s*x + N = 0
            delta = s*s - 4*N
            if(delta>=0):
                t = intSqrt(delta)
                if t!=-1 and (s+t)%2==0:
                    return d

################################################################################################################

# TEST functions

# main() to integerate the above functionality and perform tests
def main():
    print("Testing Wiener Attack")
    index = 1
    
    with open("RSA_CRACK_RESULTS.txt", 'w', encoding =  'utf-8') as f:
        f.write("**********************RSA Crack Results::**********************\n\n")
        f.write("NOTE: 36*(d^4)<n")
        for nbits in range(512, 3100, 512):
            
            f.write("\n\n************************************************************")
            f.write("\nNumber of bits in n: ")
            f.write(str(nbits))
            f.write("\n")
            for i in range(10):

                print("Generating keys")
                (N, e, d) = getKeys(nbits)
                start_time = time.clock()
                print("Keys Generated")

                f.write("\n\nTest ")
                f.write(str(i+1))
                f.write(":\n")

                f.write("\nGenerated key values: \n")
                f.write("N = ")
                f.write(str(N))
                f.write("\n")
                f.write("e = ")
                f.write(str(e))
                f.write("\n")
                f.write("d = ")
                f.write(str(d))
                f.write("\n")

                print("Cracking...")
                cracked_d = crackRSA(N, e)

                time_to_crack = time.clock() - start_time

                f.write("\nCracked private exponent, d = ")
                f.write(str(cracked_d))
                f.write("\n")

                f.write("\nTime taken: ")
                f.write(str(time_to_crack))
                f.write(" seconds")
                f.write("\n")

                if d == cracked_d:
                    f.write("######## SUCCESSFULLY CRACKED ########\n")
                    print("CRACKED!")
                else:
                    f.write("######## CRACK FAILED ########\n")
                    print("FAILED")

                index += 1

################################################################################################################

main()