import math
import numpy as np

def bp_rp_to_kelvin(bp_rp):
    # Calcula la temperatura en Kelvin a partir de BP - RP
    kelvin = 4600 * (1 / (bp_rp + 0.92)) + 4000
    return kelvin

def kelvin_to_rgb(colour_temperature: float) -> np.ndarray:
    # Range check.
    colour_temperature = np.clip(colour_temperature, 1000, 40000)

    tmp_internal = colour_temperature / 100.0

    # Red.
    if tmp_internal <= 66:
        red = 255
    else:
        red = 329.698727446 * (tmp_internal - 60)**-0.1332047592

    # Green.
    if tmp_internal <= 66:
        green = 99.4708025861 * np.log(tmp_internal) - 161.1195681661
    else:
        green = 288.1221695283 * (tmp_internal - 60)**-0.0755148492

    # Blue.
    if tmp_internal >= 66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        blue = 138.5177312231 * np.log(tmp_internal - 10) - 305.0447927307

    return np.clip((red, green, blue), 0, 255)

if __name__ == "__main__":
    # Ejemplo de uso
    bp_rp_value = 0.8180341720581055  # BP - RP
    kelvin_temp = bp_rp_to_kelvin(bp_rp_value)
    rgb_color = kelvin_to_rgb(kelvin_temp)
    print(f"RGB color for BP - RP = {kelvin_temp}k--{bp_rp_value}: {rgb_color}")