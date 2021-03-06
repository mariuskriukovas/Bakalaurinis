import git.Bakalaurinis.experiments.noise_dictionaries as noise_dict
from git.Bakalaurinis.experiments.cx_experiment import prepare_cx_gate_experiment
from git.Bakalaurinis.experiments.h_gate_experiment import prepare_h_gate_experiment
from git.Bakalaurinis.experiments.measurement_gate_experiment import prepare_measurement_gate_experiment
from git.Bakalaurinis.experiments.rotation_gate_experiments import init_p_gates, init_ry_gates, init_rx_gates, \
    init_rz_gates, prepare_full_rotation_experiment_in_interval
from git.Bakalaurinis.experiments.single_gate_noise_calculation import execute_experiment, execute_rotation_experiment
from git.Bakalaurinis.experiments.x_gate_experiment import prepare_x_gate_experiment
from git.Bakalaurinis.tools.excel_tools import append_excel_sheets
from git.Bakalaurinis.simuliator.gates import gate_factory
from git.Bakalaurinis.simuliator.gates import rx_gate, ry_gate

def execute_m_noise_calculation():
    print("execute_m_noise_calculation")

    df = execute_experiment(name='Sheet_quito_M',
                            experiments=prepare_measurement_gate_experiment(),
                            noise_dictionary=noise_dict.m_gate_quito_noise_dictionary)
    append_excel_sheets(df_arr=[df],
                        df_names=["quito_M_Aprox"])

    # df = execute_experiment(name='Sheet_yorktown_M',
    #                         experiments=prepare_measurement_gate_experiment(),
    #                         noise_dictionary=noise_dict.m_gate_yorktown_noise_dictionary)
    # append_excel_sheets(df_arr=[df],
    #                     df_names=["yorktown_M_Aprox"])

# execute_m_noise_calculation()

def execute_x_M1_noise_calculation():
    print("execute_x_M1_noise_calculation")
    df = execute_experiment(name='Sheet_quito_X',
                            experiments=prepare_x_gate_experiment(),
                            noise_dictionary=noise_dict.x_gate_quito_noise_dictionary_M1)
    append_excel_sheets(df_arr=[df],
                        df_names=["quito_X_Aprox_M1"])

    df = execute_experiment(name='Sheet_yorktown_X',
                            experiments=prepare_x_gate_experiment(),
                            noise_dictionary=noise_dict.x_gate_yorktown_noise_dictionary_M1)
    append_excel_sheets(df_arr=[df],
                        df_names=["yorktown_M_Aprox_M1"])


def execute_x_M2_noise_calculation():
    print("execute_x_M2_noise_calculation")

    df = execute_experiment(name='Sheet_quito_X',
                            experiments=prepare_x_gate_experiment(),
                            noise_dictionary=noise_dict.x_gate_quito_noise_dictionary_M2)
    append_excel_sheets(df_arr=[df],
                        df_names=["quito_X_Aprox_M2"])

    df = execute_experiment(name='Sheet_yorktown_X',
                            experiments=prepare_x_gate_experiment(),
                            noise_dictionary=noise_dict.x_gate_yorktown_noise_dictionary_M2)
    append_excel_sheets(df_arr=[df],
                        df_names=["yorktown_X_Aprox_M2"])


def execute_h_ry_noise_calculation():
    print("execute_h_ry_noise_calculation")

    df = execute_experiment(name='Sheet_h_gate_quito',
                            experiments=prepare_h_gate_experiment(),
                            noise_dictionary=noise_dict.h_gate_quito_noise_dictionary_ry)

    append_excel_sheets(df_arr=[df],
                        df_names=["quito_H_Aprox_ry"])

    df = execute_experiment(name='Sheet_h_gate_yorktown_Y',
                            experiments=prepare_h_gate_experiment(),
                            noise_dictionary=noise_dict.h_gate_yorktown_noise_dictionary_ry)

    append_excel_sheets(df_arr=[df],
                        df_names=["yorktown_H_Aprox_ry"])

# execute_h_ry_noise_calculation()

def execute_h_rx_noise_calculation():
    print("execute_h_rx_noise_calculation")

    df = execute_experiment(name='Sheet_h_gate_quito',
                            experiments=prepare_h_gate_experiment(),
                            noise_dictionary=noise_dict.h_gate_quito_noise_dictionary_rx)

    append_excel_sheets(df_arr=[df],
                        df_names=["quito_H_Aprox_ry"])

    df = execute_experiment(name='Sheet_h_gate_yorktown_Y',
                            experiments=prepare_h_gate_experiment(),
                            noise_dictionary=noise_dict.h_gate_yorktown_noise_dictionary_rx)

    append_excel_sheets(df_arr=[df],
                        df_names=["yorktown_H_Aprox_ry"])


def execute_full_rx_noise_calculation():
    # print("execute_rx_noise_calculation")
    # df = execute_rotation_experiment(name='Sheet_f_rx_gate_quito',
    #                                  experiments=prepare_full_rotation_experiment_in_interval(init_rx_gates),
    #                                  noise_dictionary=noise_dict.rx_gate_quito_noise_dictionary)
    #
    # append_excel_sheets(df_arr=[df],
    #                     df_names=["f_rx_gate_quito_Aprox"])
    #
    # print("execute_rx_noise_calculation")
    df = execute_rotation_experiment(name='Sheet_f_rx_gate_yorktown_Y',
                                     experiments=prepare_full_rotation_experiment_in_interval(init_rx_gates),
                                     noise_dictionary=noise_dict.rx_gate_yorktown_noise_dictionary)

    append_excel_sheets(df_arr=[df],
                        df_names=["f_rx_gate_yorktown_Aprox"])

# execute_full_rx_noise_calculation()

def execute_full_ry_noise_calculation():
    # print("execute_ry_noise_calculation")
    # df = execute_rotation_experiment(name='Sheet_f_ry_gate_quito',
    #                                  experiments=prepare_full_rotation_experiment_in_interval(init_ry_gates),
    #                                  noise_dictionary=noise_dict.ry_gate_quito_noise_dictionary)
    #
    # append_excel_sheets(df_arr=[df],
    #                     df_names=["f_ry_gate_quito_Aprox"])
    #
    # print("execute_ry_noise_calculation")
    df = execute_rotation_experiment(name='Sheet_f_ry_gate_yorktown_Y',
                                     experiments=prepare_full_rotation_experiment_in_interval(init_ry_gates),
                                     noise_dictionary=noise_dict.ry_gate_yorktown_noise_dictionary)

    append_excel_sheets(df_arr=[df],
                        df_names=["f_ry_gate_yorktown_Aprox"])

# execute_full_ry_noise_calculation()

def execute_full_rz_noise_calculation():
    # print("execute_rz_noise_calculation")
    # df = execute_rotation_experiment(name='Sheet_f_rz_gate_quito',
    #                                  experiments=prepare_full_rotation_experiment_in_interval(init_rz_gates),
    #                                  noise_dictionary=noise_dict.rz_gate_quito_noise_dictionary)
    #
    # append_excel_sheets(df_arr=[df],
    #                     df_names=["f_rz_gate_quito_Aprox"])

    print("execute_rz_noise_calculation")
    df = execute_rotation_experiment(name='Sheet_f_rz_gate_yorktown_Y',
                                     experiments=prepare_full_rotation_experiment_in_interval(init_rz_gates),
                                     noise_dictionary=noise_dict.rz_gate_yorktown_noise_dictionary)

    append_excel_sheets(df_arr=[df],
                        df_names=["f_rz_gate_yorktown_Aprox"])

# execute_full_rz_noise_calculation()

def execute_full_p_noise_calculation():
    # print("execute_p_noise_calculation")
    # df = execute_rotation_experiment(name='Sheet_f_p_gate_quito',
    #                                  experiments=prepare_full_rotation_experiment_in_interval(init_p_gates),
    #                                  noise_dictionary=noise_dict.p_gate_quito_noise_dictionary)
    #
    # append_excel_sheets(df_arr=[df],
    #                     df_names=["f_p_gate_quito_Aprox"])

    print("execute_p_noise_calculation")
    df = execute_rotation_experiment(name='Sheet_f_p_gate_yorktown_Y',
                                     experiments=prepare_full_rotation_experiment_in_interval(init_p_gates),
                                     noise_dictionary=noise_dict.p_gate_yorktown_noise_dictionary)

    append_excel_sheets(df_arr=[df],
                        df_names=["f_p_gate_yorktown_Aprox"])

# execute_full_p_noise_calculation()

def execute_cx_noise_calculation():
    print('execute_cx_noise_calculation')
    df = execute_experiment(name='Sheet_cx_gate_quito_o',
                            experiments=prepare_cx_gate_experiment(True),
                            noise_dictionary=noise_dict.cx_gate_quito_noise_dictionary)

    append_excel_sheets(df_arr=[df],
                        df_names=["quito_cx_x_o_Aprox"])

    df = execute_experiment(name='Sheet_cx_gate_yorktown_o_Y',
                            experiments=prepare_cx_gate_experiment(True),
                            noise_dictionary=noise_dict.cx_gate_yorktown_noise_dictionary)

    append_excel_sheets(df_arr=[df],
                        df_names=["yorktown_cx_x_o_Aprox"])

# execute_cx_noise_calculation()

def execute_experiments():
    # execute_x_M1_noise_calculation()
    # execute_x_M2_noise_calculation()
    execute_h_ry_noise_calculation()
    # execute_h_ry_noise_calculation()
    # execute_full_rx_noise_calculation()
    # execute_full_ry_noise_calculation()
    # execute_full_rz_noise_calculation()
    # execute_full_p_noise_calculation()
    # execute_cx_noise_calculation()

# execute_experiments()