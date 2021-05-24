from git.Bakalaurinis.simuliator.gates import gate_factory
from git.Bakalaurinis.simuliator.gates import rx_gate, ry_gate


def rx_gate_quito_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'TRx': i,
    }


def rx_gate_yorktown_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'TRx': i,
    }

def ry_gate_quito_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'TRy': i,
    }


def ry_gate_yorktown_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'TRy': i,
    }


def rz_gate_quito_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        # 'H': gate_factory(rx_gate, 1.48866929133858),
        'TRz': i,
    }


def rz_gate_yorktown_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        # 'H': gate_factory(rx_gate, 1.886),
        'TRz': i,
    }


def p_gate_quito_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        # 'H': gate_factory(rx_gate, 1.48866929133858),
        'TP': i,
    }


def p_gate_yorktown_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        # 'H': gate_factory(rx_gate, 1.886),
        'TP': i,
    }


def m_gate_quito_noise_dictionary(i):
    return {
        'M': gate_factory(rx_gate, i),
    }


def m_gate_yorktown_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, i),
    }


def x_gate_quito_noise_dictionary_M1(i):
    return {
        'M': gate_factory(ry_gate,  0.1971252455),
        'X': gate_factory(rx_gate, i),
    }


def x_gate_yorktown_noise_dictionary_M1(i):
    return {
        'M': gate_factory(ry_gate, 0.2543),
        'X': gate_factory(rx_gate, i),
    }


def x_gate_quito_noise_dictionary_M2(i):
    return {
        'M': gate_factory(rx_gate,  0.232),
        'X': gate_factory(rx_gate, i),
    }


def x_gate_yorktown_noise_dictionary_M2(i):
    return {
        'M': gate_factory(ry_gate, 0.2795),
        'X': gate_factory(rx_gate, i),
    }


def h_gate_quito_noise_dictionary_ry(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'H': gate_factory(ry_gate, i),
    }


def h_gate_yorktown_noise_dictionary_ry(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'H': gate_factory(ry_gate, i),
    }


def h_gate_quito_noise_dictionary_rx(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'H': gate_factory(rx_gate, i),
    }


def h_gate_yorktown_noise_dictionary_rx(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'H': gate_factory(rx_gate, i),
    }


def cx_gate_quito_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'X': gate_factory(rx_gate, 0.4143163353500435),
        # 'X': gate_factory(rx_gate, 0.3626673973234888),
        # 'X': gate_factory(rx_gate,  0.7262122199321859),
        # 'X': gate_factory(rx_gate, 0.5526578795569914),
        'CX': gate_factory(rx_gate, i),
    }


def cx_gate_yorktown_noise_dictionary(i):
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'X': gate_factory(rx_gate, 0.573896226415094),
        'CX': gate_factory(rx_gate, i),
    }
