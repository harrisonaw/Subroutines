import math
import csv
import numpy as np
import numpy.linalg as LA

yld_T = np.array([[2, -1, -1, 0, 0, 0],
                  [-1, 2, -1, 0, 0, 0],
                  [-1, -1, 2, 0, 0, 0],
                  [0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 3]])
yld_T = yld_T/3.0
c_params = np.array([-0.0698, 0.9364, 0.0791, 1.0030, 0.5247, 1.3631, 0.9543, 1.0690, 1.0237,
                     0.9811, 0.4767, 0.5753, 0.8668, 1.1450, -0.0792, 1.4046, 1.1471, 1.0516])

# AA2090-T3
# AFR
c_params = np.array([-0.39041623190900254, 1.2085606862513412, -0.022842960001355474,
                     0.41980993661904814, 0.6058009259523878, 1.24418287683899,
                     1.0560139963927146, 1.0891167207195427, 1.0937908219648715,
                     0.8929749195662852, 0.451977984957348, 0.45689003976724196,
                     0.9205647370007469, 1.1227253204886476, -0.3010616487829765,
                     1.3166540502252138, 1.1659800747052957, 1.121007094144193])
# stress
c_params = np.array([0.056940277665336686, 0.9859971641591349, 0.1986277232332533,
                     0.9313609018430112, 0.5871124291038275, 1.330942716974344,
                     0.944649833438939, 1.090740680806561, 1.0925155792832137,
                     1.0763323731674885, 0.4323653254398786, 0.613688607514406,
                     0.9659074930180515, 1.1519059774170437, -0.08362991282554624,
                     1.4567012369610057, 1.1752482654026506, 1.116415832572442])
# r
c_params = np.array([-0.0681890550605269, 0.8728581783781829, 0.07883817293470376,
                     0.9800868482532625, 0.6396161030250869, 1.416739220885185,
                     1.0767566538602826, 1.069, 1.0237,
                     0.936165230037105, 0.7827698684119997, 0.6837450696952991,
                     0.7782197960468684, 1.1210834461178005, -0.0930311520854942,
                     1.1682692085440296, 1.1471, 1.0516])

# DP980
# AFR
c_params = np.array([0.978676811742272, 1.0155655137865276, 0.9562935015714478,
                     0.9923044145704766, 1.0379668696483502, 0.9699665765886128,
                     1.0229368224938618, 1.0, 1.0,
                     0.978658158833893, 1.0156280173593986, 0.9563282984646336,
                     0.992335717702875, 1.037930467713471, 0.9699600496984562,
                     1.0229238225580262, 1.0, 1.0])
# stress
c_params = np.array([0.9821539246198124, 1.016247297800221, 0.9729007462726103,
                     0.9937171620627243, 1.025380829900888, 0.9846366340527765,
                     1.011868280897356, 1.0, 1.0,
                     0.9821429549798266, 1.0163109473834446, 0.9730928736280997,
                     0.9937337927111698, 1.0254718751198486, 0.9845101646643356,
                     1.0116904428635412, 1.0, 1.0])
# r
# c_params = np.array([0.9630755236085117, 1.0404635133877267, 0.9671641135689687,
#                      0.9666250667631737, 1.0364152750397875, 0.9707464664422254,
#                      1.0278975580349605, 1.0, 1.0,
#                      0.9630621276929356, 1.0405349522836391, 0.9671784592047932,
#                      0.9666518844943464, 1.0363759388697624, 0.9707396235439515,
#                      1.027884484472155, 1.0, 1.0])
YLDM = 6


def make_C_matrix(c_params):
    yld_C_prime = np.array([[0, -1.0*c_params[0], -1.0*c_params[1], 0, 0, 0],
                            [-1.0*c_params[2], 0, -1.0*c_params[3], 0, 0, 0],
                            [-1.0*c_params[4], -1.0*c_params[5], 0, 0, 0, 0],
                            [0, 0, 0, c_params[6], 0, 0],
                            [0, 0, 0, 0, c_params[7], 0],
                            [0, 0, 0, 0, 0, c_params[8]]])
    yld_C_Db_prime = np.array([[0, -1.0*c_params[9], -1.0*c_params[10], 0, 0, 0],
                               [-1.0*c_params[11], 0, -1.0*c_params[12], 0, 0, 0],
                               [-1.0*c_params[13], -1.0*c_params[14], 0, 0, 0, 0],
                               [0, 0, 0, c_params[15], 0, 0],
                               [0, 0, 0, 0, c_params[16], 0],
                               [0, 0, 0, 0, 0, c_params[17]]])
    return yld_C_prime, yld_C_Db_prime


def calc_phi(stress, c_params, YLDM):
    yld_C_prime, yld_C_Db_prime = make_C_matrix(c_params)
    s_prime = yld_C_prime@yld_T@stress
    s_Db_prime = yld_C_Db_prime@yld_T@stress
    s_prime_mat = np.array([[s_prime[0], s_prime[3], s_prime[4]],
                            [s_prime[3], s_prime[1], s_prime[5]],
                            [s_prime[4], s_prime[5], s_prime[2]]])
    s_Db_prime_mat = np.array([[s_Db_prime[0], s_Db_prime[3], s_Db_prime[4]],
                               [s_Db_prime[3], s_Db_prime[1], s_Db_prime[5]],
                               [s_Db_prime[4], s_Db_prime[5], s_Db_prime[2]]])
    pri_stress, _v = LA.eig(s_prime_mat)
    pri_Db_stress, _v = LA.eig(s_Db_prime_mat)
    phi = 0.0
    for i in range(3):
        for j in range(3):
            phi += abs(pri_stress[i] - pri_Db_stress[j])**YLDM

    return phi


def calc_angled_eqStress(angle, c_params, YLDM):
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
    phi = calc_phi(angled_stress, c_params, YLDM)
    angled_eqStress = (4/phi)**(1/YLDM)
    return angled_eqStress


def error_func(exp_data, c_params, YLDM, wp, wq, wb):
    error = 0
    for data in exp_data:
        angle = data["orientation"]
        if wp != 0:
            exp_eqStress = float(data["normalized_yield_stress"])
            if exp_eqStress == 0:
                continue
            predicted_stress = calc_angled_eqStress(angle, c_params, YLDM)
            if not angle.isdecimal():
                error += wb*(predicted_stress/exp_eqStress - 1.0)**2
            else:
                error += wp*(predicted_stress/exp_eqStress - 1.0)**2

        if wq != 0:
            exp_r = float(data["r_value"])
            if exp_r == 0:
                continue
            predicted_r = calc_angled_r(angle, c_params, YLDM)
            if not angle.isdecimal():
                error += wb*(predicted_r/exp_r - 1.0)**2
            else:
                error += wq*(predicted_r/exp_r - 1.0)**2

    return error


def calc_dsdc(angle, c_params, YLDM):
    DELTAX = 1.0e-6
    dsdc = np.ones(18)
    predicted_stress = calc_angled_eqStress(angle, c_params, YLDM)
    for i in range(18):
        sub_c_params = c_params.copy()
        sub_c_params[i] += DELTAX
        sub_predicted_stress = calc_angled_eqStress(angle, sub_c_params, YLDM)
        dsdc[i] = (sub_predicted_stress - predicted_stress)/DELTAX
    return dsdc


def calc_drdc(angle, c_params, YLDM):
    DELTAX = 1.0e-6
    drdc = np.ones(18)
    predicted_r = calc_angled_r(angle, c_params, YLDM)
    for i in range(18):
        sub_c_params = c_params.copy()
        sub_c_params[i] += DELTAX
        sub_predicted_r = calc_angled_r(angle, sub_c_params, YLDM)
        drdc[i] = (sub_predicted_r - predicted_r)/DELTAX
    return drdc


def calc_dphids(angle, c_params, YLDM):
    DELTAX = 1.0e-6
    dphids = np.zeros(6)
    if angle == "EB":
        angled_stress = np.array([-1/3.0, -1/3.0, 2/3.0, 0, 0, 0])
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
    phi = calc_phi(angled_stress, c_params, YLDM)
    for i in range(6):
        sub_angled_stress = angled_stress.copy()
        sub_angled_stress[i] += DELTAX
        sub_phi = calc_phi(sub_angled_stress, c_params, YLDM)
        dphids[i] = (sub_phi - phi)/DELTAX
    return dphids


def calc_dfds(angle, c_params, YLDM):
    dphids = calc_dphids(angle, c_params, YLDM)
    angled_eqStress = calc_angled_eqStress(angle, c_params, YLDM)
    dfds = (dphids*angled_eqStress**(1-YLDM))/(4*YLDM)
    return dfds


def calc_angled_r(angle, c_params, YLDM):
    dphids = calc_dphids(angle, c_params, YLDM)
    dfds = calc_dfds(angle, c_params, YLDM)
    if angle == "EB":
        r = dphids[1]/dphids[0]
    else:
        angle = math.pi*float(angle)/180.0
        r = (dfds[3]*math.cos(angle)*math.sin(angle)-dfds[0]*math.sin(angle)**2 -
             dfds[1]*math.cos(angle)**2)/(dfds[0]+dfds[1])
    return r


def calc_error_gradient(exp_data, c_params, YLDM, wp, wq, wb):
    gradient = np.zeros(18)
    for data in exp_data:
        angle = data["orientation"]

        # calculate gradient from stress
        if wp != 0:
            predicted_stress = calc_angled_eqStress(angle, c_params, YLDM)
            exp_stress = float(data["normalized_yield_stress"])
            dsdc = calc_dsdc(angle, c_params, YLDM)
            if not angle.isdecimal():
                gradient += (wb*2.0*(predicted_stress/exp_stress - 1.0)/exp_stress)*dsdc
            else:
                gradient += (wp*2.0*(predicted_stress/exp_stress - 1.0)/exp_stress)*dsdc

        # calculate gradient from Lankford value
        if wq != 0:
            if not (angle.isdecimal() or angle == "EB"):
                continue
            predicted_r = calc_angled_r(angle, c_params, YLDM)
            exp_r = float(data["r_value"])
            drdc = calc_drdc(angle, c_params, YLDM)
            if not angle.isdecimal():
                gradient += (wb*2.0*(predicted_r/exp_r - 1.0)/exp_r)*drdc
            else:
                gradient += (wq*2.0*(predicted_r/exp_r - 1.0)/exp_r)*drdc
    return gradient


def gradient_descent(exp_data, YLDM, wp, wq, wb):
    learning_rate = 1.0e-1
    c_params = np.ones(18)
    with open('Datas/errortest.csv', 'w') as f:
        writer = csv.writer(f)
        header = ["iterationNum", "error", "c_params"]
        writer.writerow(header)
        for i in range(30000):
            error = error_func(exp_data, c_params, YLDM, wp, wq, wb)
            writer.writerow([i, error, ' '.join(map(str, c_params))])
            print(i, error)
            gradient = calc_error_gradient(exp_data, c_params, YLDM, wp, wq, wb)
            c_params -= learning_rate*gradient
    return c_params


if __name__ == "__main__":
    with open("Datas/AA2090-T3.csv") as f:
        reader = csv.DictReader(f)
        exp_data = [row for row in reader]
    wp = 1.0
    wq = 0.1
    wb = 0.01
    # c_params = gradient_descent(exp_data, YLDM, wp, wq, wb)
    # print(c_params)
    # for angle in ["0", "15", "30", "45", "60", "75", "90", "EB"]:
    #     print(angle)
    #     print("stress", calc_angled_eqStress(angle, c_params, YLDM))
    #     print("r", calc_angled_r(angle, c_params, YLDM))
    for angle in ["TDND", "TDND45", "NDRD", "NDRD45"]:
        print(angle)
        print("stress", calc_angled_eqStress(angle, c_params, YLDM))
