class InstrumentConfig:
    DEFAULT_ADDRESS = 9
    TIMEOUT_MS = 10_000
    PLC_MAX = 500
    NPLC_MIN = 0.001  # 20 microseconds at 50Hz
    GPIB_PREFIX = "GPIB0::"
    GPIB_SUFFIX = "::INSTR"
    ROOT_DCV = ":VOLT:DC"
    ROOT_DCI = ":CURR:DC"
    RANGE_MODE_AUTO = 1
    RANGE_MODE_MAN = 0
    RANGE_MODE_AUTO_STR = "AUTO"
    RANGE_MODE_MAN_STR = "MAN"

    # Instrument-defined valid values — used by Fluke8588A for input validation
    VALID_APERTURE_MODES = {"AUTO", "FAST", "MAN"}
    VALID_IMPEDANCES_DCV = {"AUTO", "1M", "10M"}
    VALID_RESOLUTIONS_DC = {1e-4, 1e-5, 1e-6, 1e-7, 1e-8}
    VALID_RESOLUTIONS_DC_DIGITS = {4, 5, 6, 7, 8}
    VALID_RESOLUTIONS_AC = {1e-4, 1e-5, 1e-6, 1e-7}
    VALID_RESOLUTIONS_AC_DIGITS = {4, 5, 6, 7}