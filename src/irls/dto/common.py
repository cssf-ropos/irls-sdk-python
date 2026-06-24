"""Shared types used across multiple sensor APIs."""

from enum import StrEnum


class ScientificUnit(StrEnum):
    # Temperature
    DEGREES_CELSIUS = "degrees_celsius"
    DEGREES_FAHRENHEIT = "degrees_fahrenheit"
    KELVIN = "kelvin"
    # Conductivity
    SIEMENS_PER_METER = "siemens_per_meter"
    MILLISIEMENS_PER_CENTIMETRE = "millisiemens_per_centimetre"
    # Pressure
    DECIBAR = "decibar"
    BAR = "bar"
    KILOPASCAL = "kilopascal"
    PSI = "psi"
    # Salinity
    PSU = "psu"
    # Oxygen
    MICROMOL_PER_LITRE = "micromol_per_litre"
    MILLILITRES_PER_LITRE = "millilitres_per_litre"
    MILLIGRAMS_PER_LITRE = "milligrams_per_litre"
    PERCENT_SATURATION = "percent_saturation"
    # Velocity / Depth
    METRES_PER_SECOND = "metres_per_second"
    METRES = "metres"
    # Turbidity
    NTU = "ntu"
    FNU = "fnu"
    # Density
    KILOGRAMS_PER_CUBIC_METRE = "kilograms_per_cubic_metre"
    # Optical / Bio
    MICROGRAMS_PER_LITRE = "micrograms_per_litre"
    RELATIVE_FLUORESCENCE_UNITS = "relative_fluorescence_units"
    MICROMOL_PHOTONS_PER_M2_PER_S = "micromol_photons_per_m2_per_s"
    # Dimensionless
    PH = "ph"
    PERCENT = "percent"
