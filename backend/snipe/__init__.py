__app_name__="snipe-engine"
__version__="0.1.0"


(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    AVRO_READ_ERROR,
    AVRO_WRITE_ERROR
) = range(5)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    AVRO_READ_ERROR: "avro read error",
    AVRO_WRITE_ERROR: "avro write error"
}

