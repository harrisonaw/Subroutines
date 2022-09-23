import csv
import math
import numpy as np


yld_T = np.array([[2, -1, -1, 0, 0, 0],
                  [-1, 2, -1, 0, 0, 0],
                  [-1, -1, 2, 0, 0, 0],
                  [0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 3]])
yld_T = yld_T/3.0

# AA2090-T3
# f
# hill_params = np.array([0.570281847241541, 0.3632288531248622,
#                         0.6367711468751378, 2.5710503236965727])
# g
# hill_params = np.array([0.25216953733566727, 0.8254230293025175,
#                         0.17457697069748246, 2.2380520016508463])

# DP980
# f
hill_params = np.array([0.4844687812695614, 0.5441303900909464,
                        0.4558696099090537, 1.5201303973492752])

# g
# hill_params = np.array([0.42610421732178394, 0.5913660555884093,
#                         0.4086339444115908, 1.5770789230107995])


def calc_eqStress(stress, hill_params):
    numerator = 0
    stress = yld_T@stress
    for i in range(3):
        numerator += hill_params[i]*(stress[(i+1) % 3]-stress[(i+2) % 3])**2
        numerator += 2*hill_params[3]*stress[i+3]**2
    return math.sqrt(numerator*1.5/sum(hill_params[:3]))


def calc_angled_eqStress(angle, hill_params):
    if angle == "EB":
        angled_stress = np.array([0, 0, 1, 0, 0, 0])
    elif angle == "TDND":
        angled_stress = np.array([0, 0, 0, 0, 0, 1.0])
    elif angle == "NDRD":
        angled_stress = np.array([0, 0, 0, 0, 1.0, 0])
    elif angle == "TDND45":
        angled_stress = np.array([0, 0.5, 0.5, 0, 0, 0.5])
    elif angle == "NDRD45":
        angled_stress = np.array([0.5, 0, 0.5, 0, 0.5, 0])
    else:
        angle = math.pi*float(angle)/180.0
        angled_stress = np.array([math.cos(angle)**2, math.sin(angle)**2,
                                  0, math.sin(angle)*math.cos(angle), 0, 0])
    angled_eqStress = 1/calc_eqStress(angled_stress, hill_params)
    return angled_eqStress


def calc_dfds(angle, hill_params):
    # analytical method
    dfds = np.ones(6)
    if angle == "EB":
        angled_stress = np.array([0, 0, 1, 0, 0, 0])
    elif angle == "TDND":
        angled_stress = np.array([0, 0, 0, 0, 0, 1.0])
    elif angle == "NDRD":
        angled_stress = np.array([0, 0, 0, 0, 1.0, 0])
    elif angle == "TDND45":
        angled_stress = np.array([0, 0.5, 0.5, 0, 0, 0.5])
    elif angle == "NDRD45":
        angled_stress = np.array([0.5, 0, 0.5, 0, 0.5, 0])
    else:
        angle = math.pi*float(angle)/180.0
        angled_stress = np.array([math.cos(angle)**2, math.sin(angle)**2,
                                  0, math.sin(angle)*math.cos(angle), 0, 0])
    angled_eqStress = calc_angled_eqStress(angle, hill_params)
    multiplier = 0.75/(sum(hill_params[:3])*angled_eqStress)
    dfds[0] = -2*hill_params[1]*(angled_stress[2] - angled_stress[0]) + \
        2*hill_params[2]*(angled_stress[0]-angled_stress[1])
    dfds[1] = 2*hill_params[0]*(angled_stress[1]-angled_stress[2]) - \
        2*hill_params[2]*(angled_stress[0]-angled_stress[1])
    dfds[2] = -2*hill_params[0]*(angled_stress[1]-angled_stress[2]) + \
        2*hill_params[1]*(angled_stress[2]-angled_stress[0])
    dfds[3] = 4*hill_params[3]*angled_stress[3]
    dfds[4] = 4*hill_params[3]*angled_stress[4]
    dfds[5] = 4*hill_params[3]*angled_stress[5]
    dfds *= multiplier
    return dfds


def calc_angled_r(angle, hill_params):
    dfds = calc_dfds(angle, hill_params)
    if angle == "EB":
        r = dfds[1]/dfds[0]
    else:
        angle = math.pi*float(angle)/180.0
        r = (dfds[3]*math.cos(angle)*math.sin(angle)-dfds[0]*math.sin(angle)**2 -
             dfds[1]*math.cos(angle)**2)/(dfds[0]+dfds[1])
    return r


def calc_hill_params():
    with open("Datas/DP980.csv") as f:
        reader = csv.DictReader(f)
        exp_data = [row for row in reader]

    for data in exp_data:
        orientation = data["orientation"]
        yield_stress = float(data["normalized_yield_stress"])
        r_value = float(data["r_value"])
        if orientation == "0":
            s0 = yield_stress
            r0 = r_value
        elif orientation == "45":
            s45 = yield_stress
            r45 = r_value
        elif orientation == "90":
            s90 = yield_stress
            r90 = r_value
        elif orientation == "EB":
            sb = yield_stress
            # rb = r_value

    stressF = (1/s90**2 + 1/sb**2 - 1/s0**2)/2
    stressG = (1/sb**2 + 1/s0**2 - 1/s90**2)/2
    stressH = (1/s0**2 + 1/s90**2 - 1/sb**2)/2
    stressN = ((2/s45)**2 - (1/sb)**2)/2
    hill_f_params = np.array([stressF, stressG, stressH, stressN])
    print("stressF", stressF)
    print("stressG", stressG)
    print("stressH", stressH)
    print("stressN", stressN)

    rF = r0/(r90*(1.0+r0))
    rG = 1.0/(1.0+r0)
    rH = r0/(1.0+r0)
    rN = 0.5*(r0+r90)*(1.0+2.0*r45)/(r90*(1.0+r0))
    hill_g_params = np.array([rF, rG, rH, rN])
    print("rF", rF)
    print("rG", rG)
    print("rH", rH)
    print("rN", rN)
    return hill_f_params, hill_g_params


if __name__ == "__main__":
    # hill_f_params, hill_g_params = calc_hill_params()
    # for angle in ["0", "15", "30", "45", "60", "75", "90", "EB"]:
    #     print(angle)
    #     print("stress", calc_angled_eqStress(angle, hill_params))
    #     print("r", calc_angled_r(angle, hill_params))
    for angle in ["TDND", "TDND45", "NDRD", "NDRD45"]:
        print(angle)
        print("stress", calc_angled_eqStress(angle, hill_params))
