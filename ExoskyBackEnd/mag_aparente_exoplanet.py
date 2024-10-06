import math

def absolute_mag(phot_g_mean_mag, distance_gspphot):
    absolute_mag = phot_g_mean_mag - (5 * math.log10(distance_gspphot)) + 5
    return absolute_mag

def aparent_mag_from_exoplanet(absolute_mag, distance_from_exoplanet):
    aparent_mag = absolute_mag + (5 * math.log10(distance_from_exoplanet)) - 5
    return aparent_mag

if __name__ == "__main__":
    phot_g_mean_mag = 6.763094902038574
    distance_from_earth = 24.995100021362305
    distance_from_exoplanet = 8.923878165852768
    absolute_mag_star = absolute_mag(phot_g_mean_mag, distance_from_earth)
    aparent_mag_exoplanet = aparent_mag_from_exoplanet(absolute_mag_star, distance_from_exoplanet)
    print(f"absolute_mag={absolute_mag_star}--aparent_fromEarth{phot_g_mean_mag}--aparent_fromExoplanet{aparent_mag_exoplanet}")