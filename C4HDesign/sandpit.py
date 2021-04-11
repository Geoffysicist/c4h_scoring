def binomial_coeffs(n: int) -> list:
    coeffs = [1]
    for k in range(n):
        coeffs.append(int((coeffs[k]*(n-k))/(k+1)))
    return coeffs

if __name__ == '__main__':
    for i in range(1,10):
        print(binomial_coeffs(i))