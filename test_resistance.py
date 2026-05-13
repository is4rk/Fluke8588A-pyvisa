import logging
from Fluke8588A import Fluke8588A
from config import InstrumentConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def test_resistance():
    """
    Simple test for resistance measurement with Fluke 8588A.
    """
    try:
        # Connect and identify
        fluke = Fluke8588A(InstrumentConfig.DEFAULT_ADDRESS)
        print(f"Instrument: {fluke.identify()}")
        
        # Configure for resistance measurement (2-wire, AUTO range)
        fluke.init_resistance(
            aperture_mode="AUTO",
            time_val=1,
            wire_mode_val="NORMal",
            low_mode_val=0,
            range_mode="AUTO",
            range_val="AUTO",
            resolution_val=4,
            filter_val=0
        )
        
        # Take measurement
        reading = fluke.read()
        print(f"Resistance: {reading}")
        funct=":FUNC \"" + ":CURR:DC"+ "\""
        funct= fluke.query(":FUNC?")
        print(funct)
        fluke.close()
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    test_resistance()
