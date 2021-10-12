from fdlibm import __HI, __LO, __HI2, __LO2

one = 1.0
half = [0.5, -0.5]
huge = 1.0e+300
huge = 1.0e+300
twom1000 = 9.33263618503218878990e-302  # 2**-1000=0x01700000,0
o_threshold = 7.09782712893383973096e+02  # 0x40862E42, 0xFEFA39EF
u_threshold = -7.45133219101941108420e+02  # 0xc0874910, 0xD52D3051
ln2HI = [6.93147180369123816490e-01,  # 0x3fe62e42, 0xfee00000 */
         -6.93147180369123816490e-01]  # 0xbfe62e42, 0xfee00000 */
ln2LO = [1.90821492927058770002e-10,  # 0x3dea39ef, 0x35793c76 */
         -1.90821492927058770002e-10]  # 0xbdea39ef, 0x35793c76 */
invln2 = 1.44269504088896338700e+00  # 0x3ff71547, 0x652b82fe */
P1 = 1.66666666666666019037e-01  # 0x3FC55555, 0x5555553E */
P2 = -2.77777777770155933842e-03  # 0xBF66C16C, 0x16BEBD93 */
P3 = 6.61375632143793436117e-05  # 0x3F11566A, 0xAF25DE2C */
P4 = -1.65339022054652515390e-06  # 0xBEBBBD41, 0xC5D26BF1 */
P5 = 4.13813679705723846039e-08  # 0x3E663769, 0x72BEA4D0 */


def __ieee754_exp(x):
    """

    :param x: The float to calculate exponential for
    :return: The exponential
    """
    y = 0.0
    hi = 0.0
    lo = 0.0
    c = 0.0
    t = 0.0
    k = 0
    xsb = 0

    hx = __HI(x)  # high word of x
    xsb = (hx >> 31) & 1  # sign bit of x
    hx &= 0x7fffffff  # high word of |x|

    if hx >= 0x40862E42:  # if |x| >= 709.78
        if hx >= 0x7ff00000:
            if ((hx & 0xfffff) | __LO(x)) != 0:
                return x + x  # NaN
            else:
                return x if xsb == 0 else 0.0  # exp(+-inf) = {inf, 0}
        if x > o_threshold:
            return huge * huge  # overflow
        if x < u_threshold:
            return twom1000 * twom1000  # underflow

    if hx > 0x3fd62e42:
        if hx < 0x3FF0A2B2:
            hi = x - ln2HI[xsb]
            lo = ln2LO[xsb]
            k = 1 - xsb - xsb
        else:
            k = int(invln2 * x + half[xsb])
            t = k
            hi = x - t * ln2HI[0]
            lo = t * ln2LO[0]

        x = hi - lo
    elif hx < 0x3e300000:
        if huge + x > one:
            return one + x
    else:
        k = 0

    t = x * x
    c = x - t * (P1 + t * (P2 + t * (P3 + t * (P4 + t * P5))))
    if k == 0:
        return one - ((x * c) / (c - 2.0) - x)
    else:
        y = one - ((lo - (x * c) / (2.0 - c)) - hi)
    if k >= -1021:
        y = __HI2(y, __HI(y) + (k << 20))
        return y
    else:
        y = __HI2(y, __HI(y) + ((k + 1000) << 20))
        return y * twom1000


# if __name__ == '__main__':
#     print(__ieee754_exp(25))
#     import math
#     print(math.exp(25))
