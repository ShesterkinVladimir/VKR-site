from numpy import array, sin, cos, tan, radians, degrees, sqrt, pi, arccos, arctan, fmax, fmin, \
    sum, concatenate, arange
# import pandas as pd
# import matplotlib.pyplot as plt


def fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth):  # основная функция расчета
    try:
        t1 = array([i for i in range(len(num_day_y))])
        # t2 = np.array(range[1, 25])
        delta = 23.45 * sin(radians(360 * (284 + num_day_y) / 365))   # delta in degrees

        a = (sin(radians(latitude)) * cos(radians(tilt_angle)) -
             cos(radians(latitude)) * sin(radians(tilt_angle))
             * cos(radians(azimuth))) * sin(radians(delta))   # a in radians

        b = (cos(radians(latitude)) * cos(radians(tilt_angle)) + sin(radians(latitude)) * sin(radians(tilt_angle))
             * cos(radians(azimuth))) * cos(radians(delta))   # a in radians

        c = sin(radians(tilt_angle)) * sin(radians(azimuth)) * cos(radians(delta))   # c in radians

        omega3 = degrees(arccos(-tan(radians(latitude)) * tan(radians(delta))))   # omega3 in degrees

        omegaB = degrees(-arccos(-tan(radians(latitude)) * tan(radians(delta))))   # omegaB in degrees

        c_a_b = c ** 2 - a ** 2 + b ** 2
        c_a_b[c_a_b < 0] = 0  # чтобы под коренм не было нуля

        a_b = a - b

        _2arctg_ABC_minus = 2 * arctan(-c - sqrt(c_a_b) / a_b)   # in radians

        _2arctg_ABC_plus = 2 * arctan(-c + sqrt(c_a_b) / a_b)   # in radians

        omega3_By = fmax(omega3, _2arctg_ABC_minus * 180 / pi)   # in degrees

        omegaB_By = fmax(omegaB, _2arctg_ABC_plus * 180 / pi)   # in degrees

        omega1 = fmin(omega3, fmax(omegaB, 15 * (t1 % 24 - 12)))   # in degrees

        omega2 = fmin(omega3, fmax(omegaB, 15 * (t1 % 24 - 11)))   # in degrees

        omega1_By = fmin(omega3_By, fmax(omegaB_By, 15 * (t1 % 24 - 12)))   # in degrees

        omega2_By = fmin(omega3_By, fmax(omegaB_By, 15 * (t1 % 24 - 11)))   # in degrees

        kpr1 = b * (sin(radians(omega2_By)) - sin(radians(omega1_By)))   # in o.e

        kpr2 = a * pi / 180 * (omega2_By - omega1_By)  # in o.e

        kpr3 = c * (cos(radians(omega2_By)) - cos(radians(omega1_By)))   # in o.e

        kpr4 = cos(radians(latitude)) * cos(radians(delta)) * (sin(radians(omega2)) - sin(radians(omega1)))   # in o.e

        omeg2_omeg1 = (omega2 - omega1) * pi / 180
        kpr5 = sin(radians(latitude)) * sin(radians(delta)) * omeg2_omeg1  # in o.e

        kpr = []
        for i in range(len(num_day_y)):
            if kpr4[i] + kpr5[i] != 0:
                kpr.append((kpr1[i] + kpr2[i] - kpr3[i]) / (kpr4[i] + kpr5[i]))
            else:
                kpr.append(0)
        kpr = array(kpr)

        r_pr = kpr * (e_sum - e_dif)

        r_d = e_dif * (180 - tilt_angle) / 180

        r_otr = 0.5 * ro * e_sum * sin(radians(tilt_angle))

        r = r_pr + r_d + r_otr

        return r
    except TypeError:
        return False


# 3 функции расчета дня(график есть), месяца(график 2 +-) и года по часам(слишком много точек)
def calc_day_by_hours(data, num_month, num_day_m, latitude=0, tilt_angle=0, azimuth=0, ghi="GHI",
                      dhi="DHI", albedo="Albedo", doy="DOY"):
    e_sum = array(data[(data.Month == num_month) & (data.Day == num_day_m)][ghi])
    e_dif = array(data[(data.Month == num_month) & (data.Day == num_day_m)][dhi])
    ro = array(data[(data.Month == num_month) & (data.Day == num_day_m)][albedo])
    num_day_y = array(data[(data.Month == num_month) & (data.Day == num_day_m)][doy])
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


def calc_month_by_hours(data, num_month, latitude=0, tilt_angle=0, azimuth=0):
    e_sum = array(data[(data.Month == num_month)].GHI)
    e_dif = array(data[(data.Month == num_month)].DHI)
    ro = array(data[(data.Month == num_month)].Albedo)
    num_day_y = array(data[(data.Month == num_month)].DOY)
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


def calc_year_by_hours(data, latitude=0, tilt_angle=0, azimuth=0):
    e_sum = array(data.GHI)
    e_dif = array(data.DHI)
    ro = array(data.Albedo)
    num_day_y = array(data.DOY)
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


# Расчет месяца по дням(график есть)
def calc_month_by_day(data, num_month, latitude=0, tilt_angle=0, azimuth=0):
    month_by_hours = calc_month_by_hours(data, num_month, latitude, tilt_angle, azimuth)
    month_by_day = sum(month_by_hours.reshape(data[(data.Month == num_month)].Day.max(), 24), axis=1)
    return month_by_day


# Расчет года по месяцам(график есть)
def calc_year_by_month(data, latitude=0, tilt_angle=0, azimuth=0):
    year_by_month = []
    for num_month in range(1, 13):
        year_by_month.append(sum(calc_month_by_hours(data, num_month, latitude, tilt_angle, azimuth)))
    return array(year_by_month)


# Расчет года по дням(график 2 +-)
def calc_year_by_day(data, latitude=0, tilt_angle=0, azimuth=0):
    year_by_day = array([])
    for num_month in range(1, 13):
        year_by_day = concatenate((year_by_day, calc_month_by_day(data, num_month, latitude, tilt_angle, azimuth)))
    return year_by_day


# расчет по замкнутому интервалу(если не задавать параметры, то расчет по году)
def calc_by_range(data, num_month_start=1, num_day_m_start=1, num_month_end=12,
                  num_day_m_end=31, latitude=0, tilt_angle=0, azimuth=0):

    e_sum = array(data[(data.Month >= num_month_start) & (data.Day >= num_day_m_start) &
                       (data.Month <= num_month_end) & (data.Day <= num_day_m_end)].GHI)

    e_dif = array(data[(data.Month >= num_month_start) & (data.Day >= num_day_m_start) &
                       (data.Month <= num_month_end) & (data.Day <= num_day_m_end)].DHI)

    ro = array(data[(data.Month >= num_month_start) & (data.Day >= num_day_m_start) &
                    (data.Month <= num_month_end) & (data.Day <= num_day_m_end)].Albedo)

    num_day_y = array(data[(data.Month >= num_month_start) & (data.Day >= num_day_m_start) &
                           (data.Month <= num_month_end) & (data.Day <= num_day_m_end)].DOY)
    return fun_calc_new(num_day_y, e_sum, e_dif, ro, latitude, tilt_angle, azimuth)


# поиск угла при котором выработка максимальна (день, месяц, год или произвольный период)
def max_tilt_angle(fun, *args, latitude, azimuth):
    maximum = sum(fun(*args))
    angle = 0
    for i in range(1, 91):
        temp = sum(fun(*args, tilt_angle=i, latitude=latitude, azimuth=azimuth))  # выход не сразу
        if temp < maximum:
            break
        maximum = temp
        angle = i
    return angle, maximum

# График - дня по часам, месяца по дням и года по месяам
# def plot_for_sum(fun, *month_day):
#     fun = fun(*month_day)
#     len_args = len(month_day)
#     if len_args == 2:
#         month = month_day[0]
#         day = month_day[1]
#     elif len_args == 1:
#         month = month_day[0]
#         day = 0
#     else:
#         month = 0
#         day = 0
#
#     fig = plt.figure(figsize=(10, 6))
#     ax = fig.add_subplot()
#     plt.xticks(arange(1, len(fun) + 1, 1))
#     ax.plot([i for i in range(1, len(fun)+1)], fun, linewidth=2, marker='.', markersize=10, markeredgecolor='black')
#     # ax.set_facecolor('seashell')
#     # fig.set_facecolor('floralwhite')
#     ax.grid()
#     ax.minorticks_on()
#     ax.grid(axis ='y', which='minor',
#             color='k', linestyle=':',alpha=0.2)
#
#     if month == 0 and day == 0:
#         ax.set_title(f'Полученная энергия на наклонной поверхности за год',
#                         fontsize=13, pad='10', fontfamily='monospace', fontstyle='normal')
#         ax.set_xlabel('Месяц', fontsize=10, labelpad=8)
#
#     elif day == 0:
#         ax.set_title(f'Полученная энергия на наклонной поверхности за {month}-й месяц',
#                         fontsize=13, pad='10', fontfamily='monospace', fontstyle='normal')
#         ax.set_xlabel('День', fontsize=10, labelpad=8)
#     else:
#         ax.set_title(f'Полученная энергия на наклонной поверхности за {day}-й день {month}-го месяца',
#                     fontsize=13, pad='10', fontfamily='monospace', fontstyle='normal')
#         ax.set_xlabel('Час', fontsize=10, labelpad=8)
#
#     ax.set_ylabel('Энергия', fontsize=10, labelpad=8)
#     # plt.savefig("мой график.svg", bbox_inches='tight')
#     plt.savefig('/Users/vladimirshesterkin/PycharmProjects/vkr/sitevkr/media/testplot.png', facecolor=red)
#     return


# def plot_2(fun, month=0):
#     fig = plt.figure(figsize=(50, 25))
#     ax = fig.add_subplot()
#     ax.plot([i for i in range(1, len(fun)+1)], fun, linewidth=2)
#     # ax.set_facecolor('seashell')
#     # fig.set_facecolor('floralwhite')
#     ax.set_title(f'Полученная энергия на наклонной поверхности за {month}-ый месяц',
#                     fontsize=30, pad='10', fontfamily='monospace', fontstyle='normal')
#     ax.grid()
#     ax.minorticks_on()
#     ax.grid(which='minor',
#             color='k',linestyle=':', alpha=0.3)
#     plt.tick_params(axis='both', which='major', labelsize=25)
#     ax.set_xlabel('Часы', fontsize=30, labelpad=8)
#     ax.set_ylabel('Энергия', fontsize=30, labelpad=8)
#     # plt.savefig("g1.svg", bbox_inches='tight') #  ГИСТОГРАМА
#
#     plt.savefig('media/testplot.png')
#     return


# def max_azimuth_tilt_angle(fun, *args): # поиск максимума при изменении ушла и азимута (очень медленно)
#     maximum = sum(fun(*args))
#     angle = 0
#     azimuth = 0
#     for i in range(1, 91):
#         for j in range(1, 360):
#             temp = sum(fun(*args, tilt_angle=i, azimuth=j))
#             if temp > maximum:
#                 print(angle, azimuth, maximum)
#                 maximum = temp
#                 angle = i
#                 azimuth = j
#
#     return angle, azimuth, maximum

# dat = pd.read_csv("/Users/vladimirshesterkin/PycharmProjects/vkr/sitevkr/media/csv/test.csv", decimal=",", delimiter=';')
# calc_month_by_day(dat, 5)