from uuid import UUID

from .base import CharacteristicType, Permission

AccessoryFlags = CharacteristicType[int](
    UUID("000000A6-0000-1000-8000-0026BB765291"),
    description="Accessory Flags",
    format="uint32",
    permissions=(Permission.PAIRED_READ,),
)
Active = CharacteristicType[int](
    UUID("000000B0-0000-1000-8000-0026BB765291"),
    description="Active",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
AdministratorOnlyAccess = CharacteristicType[bool](
    UUID("00000001-0000-1000-8000-0026BB765291"),
    description="Administrator Only Access",
    format="bool",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
AirParticulateDensity = CharacteristicType[float](
    UUID("00000064-0000-1000-8000-0026BB765291"),
    description="Air Particulate Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
AirParticulateSize = CharacteristicType[int](
    UUID("00000065-0000-1000-8000-0026BB765291"),
    description="Air Particulate Size",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
AirQuality = CharacteristicType[int](
    UUID("00000095-0000-1000-8000-0026BB765291"),
    description="Air Quality",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3, 4, 5),
)
AudioFeedback = CharacteristicType[bool](
    UUID("00000005-0000-1000-8000-0026BB765291"),
    description="Audio Feedback",
    format="bool",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
BatteryLevel = CharacteristicType[int](
    UUID("00000068-0000-1000-8000-0026BB765291"),
    description="Battery Level",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
Brightness = CharacteristicType[int](
    UUID("00000008-0000-1000-8000-0026BB765291"),
    description="Brightness",
    format="int32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
CarbonDioxideDetected = CharacteristicType[int](
    UUID("00000092-0000-1000-8000-0026BB765291"),
    description="Carbon Dioxide Detected",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
CarbonDioxideLevel = CharacteristicType[float](
    UUID("00000093-0000-1000-8000-0026BB765291"),
    description="Carbon Dioxide Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=100000,
)
CarbonDioxidePeakLevel = CharacteristicType[float](
    UUID("00000094-0000-1000-8000-0026BB765291"),
    description="Carbon Dioxide Peak Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=100000,
)
CarbonMonoxideDetected = CharacteristicType[int](
    UUID("00000069-0000-1000-8000-0026BB765291"),
    description="Carbon Monoxide Detected",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
CarbonMonoxideLevel = CharacteristicType[float](
    UUID("00000090-0000-1000-8000-0026BB765291"),
    description="Carbon Monoxide Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=100,
)
CarbonMonoxidePeakLevel = CharacteristicType[float](
    UUID("00000091-0000-1000-8000-0026BB765291"),
    description="Carbon Monoxide Peak Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=100,
)
ChargingState = CharacteristicType[int](
    UUID("0000008F-0000-1000-8000-0026BB765291"),
    description="Charging State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
ColorTemperature = CharacteristicType[int](
    UUID("000000CE-0000-1000-8000-0026BB765291"),
    description="Color Temperature",
    format="uint32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    min_value=140,
    max_value=500,
    min_step=1,
)
ContactSensorState = CharacteristicType[int](
    UUID("0000006A-0000-1000-8000-0026BB765291"),
    description="Contact Sensor State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
CoolingThresholdTemperature = CharacteristicType[float](
    UUID("0000000D-0000-1000-8000-0026BB765291"),
    description="Cooling Threshold Temperature",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="celsius",
    min_value=10,
    max_value=35,
    min_step=0.1,
)
CurrentAirPurifierState = CharacteristicType[int](
    UUID("000000A9-0000-1000-8000-0026BB765291"),
    description="Current Air Purifier State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
CurrentAmbientLightLevel = CharacteristicType[float](
    UUID("0000006B-0000-1000-8000-0026BB765291"),
    description="Current Ambient Light Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    unit="lux",
    min_value=0.0001,
    max_value=100000,
)
CurrentDoorState = CharacteristicType[int](
    UUID("0000000E-0000-1000-8000-0026BB765291"),
    description="Current Door State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3, 4),
)
CurrentFanState = CharacteristicType[int](
    UUID("000000AF-0000-1000-8000-0026BB765291"),
    description="Current Fan State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
CurrentHeaterCoolerState = CharacteristicType[int](
    UUID("000000B1-0000-1000-8000-0026BB765291"),
    description="Current Heater Cooler State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3),
)
CurrentHeatingCoolingState = CharacteristicType[int](
    UUID("0000000F-0000-1000-8000-0026BB765291"),
    description="Current Heating Cooling State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
CurrentHorizontalTiltAngle = CharacteristicType[int](
    UUID("0000006C-0000-1000-8000-0026BB765291"),
    description="Current Horizontal Tilt Angle",
    format="int32",
    permissions=(Permission.PAIRED_READ,),
    unit="arcdegrees",
    min_value=-90,
    max_value=90,
    min_step=1,
)
CurrentHumidifierDehumidifierState = CharacteristicType[int](
    UUID("000000B3-0000-1000-8000-0026BB765291"),
    description="Current Humidifier Dehumidifier State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3),
)
CurrentPosition = CharacteristicType[int](
    UUID("0000006D-0000-1000-8000-0026BB765291"),
    description="Current Position",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
CurrentRelativeHumidity = CharacteristicType[float](
    UUID("00000010-0000-1000-8000-0026BB765291"),
    description="Current Relative Humidity",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
CurrentSlatState = CharacteristicType[int](
    UUID("000000AA-0000-1000-8000-0026BB765291"),
    description="Current Slat State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
CurrentTemperature = CharacteristicType[float](
    UUID("00000011-0000-1000-8000-0026BB765291"),
    description="Current Temperature",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    unit="celsius",
    min_value=0,
    max_value=100,
    min_step=0.1,
)
CurrentTiltAngle = CharacteristicType[int](
    UUID("000000C1-0000-1000-8000-0026BB765291"),
    description="Current Tilt Angle",
    format="int32",
    permissions=(Permission.PAIRED_READ,),
    unit="arcdegrees",
    min_value=-90,
    max_value=90,
    min_step=1,
)
CurrentVerticalTiltAngle = CharacteristicType[int](
    UUID("0000006E-0000-1000-8000-0026BB765291"),
    description="Current Vertical Tilt Angle",
    format="int32",
    permissions=(Permission.PAIRED_READ,),
    unit="arcdegrees",
    min_value=-90,
    max_value=90,
    min_step=1,
)
DigitalZoom = CharacteristicType[float](
    UUID("0000011D-0000-1000-8000-0026BB765291"),
    description="Digital Zoom",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
FilterChangeIndication = CharacteristicType[int](
    UUID("000000AC-0000-1000-8000-0026BB765291"),
    description="Filter Change Indication",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
FilterLifeLevel = CharacteristicType[float](
    UUID("000000AB-0000-1000-8000-0026BB765291"),
    description="Filter Life Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=100,
)
FirmwareRevision = CharacteristicType[str](
    UUID("00000052-0000-1000-8000-0026BB765291"),
    description="Firmware Revision",
    format="string",
    permissions=(Permission.PAIRED_READ,),
)
HardwareRevision = CharacteristicType[str](
    UUID("00000053-0000-1000-8000-0026BB765291"),
    description="Hardware Revision",
    format="string",
    permissions=(Permission.PAIRED_READ,),
)
HeatingThresholdTemperature = CharacteristicType[float](
    UUID("00000012-0000-1000-8000-0026BB765291"),
    description="Heating Threshold Temperature",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="celsius",
    min_value=0,
    max_value=25,
    min_step=0.1,
)
HoldPosition = CharacteristicType[bool](
    UUID("0000006F-0000-1000-8000-0026BB765291"),
    description="Hold Position",
    format="bool",
    permissions=(Permission.PAIRED_WRITE,),
)
Hue = CharacteristicType[float](
    UUID("00000013-0000-1000-8000-0026BB765291"),
    description="Hue",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="arcdegrees",
    min_value=0,
    max_value=360,
    min_step=1,
)
Identify = CharacteristicType[bool](
    UUID("00000014-0000-1000-8000-0026BB765291"),
    description="Identify",
    format="bool",
    permissions=(Permission.PAIRED_WRITE,),
)
ImageMirroring = CharacteristicType[bool](
    UUID("0000011F-0000-1000-8000-0026BB765291"),
    description="Image Mirroring",
    format="bool",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
ImageRotation = CharacteristicType[float](
    UUID("0000011E-0000-1000-8000-0026BB765291"),
    description="Image Rotation",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="arcdegrees",
    min_value=0,
    max_value=270,
    min_step=90,
)
InUse = CharacteristicType[int](
    UUID("000000D2-0000-1000-8000-0026BB765291"),
    description="In Use",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
IsConfigured = CharacteristicType[int](
    UUID("000000D6-0000-1000-8000-0026BB765291"),
    description="Is Configured",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
LeakDetected = CharacteristicType[int](
    UUID("00000070-0000-1000-8000-0026BB765291"),
    description="Leak Detected",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
LockControlPoint = CharacteristicType[bytes](
    UUID("00000019-0000-1000-8000-0026BB765291"),
    description="Lock Control Point",
    format="tlv8",
    permissions=(Permission.PAIRED_WRITE,),
)
LockCurrentState = CharacteristicType[int](
    UUID("0000001D-0000-1000-8000-0026BB765291"),
    description="Lock Current State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3),
)
LockLastKnownAction = CharacteristicType[int](
    UUID("0000001C-0000-1000-8000-0026BB765291"),
    description="Lock Last Known Action",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3, 4, 5, 6, 7, 8),
)
LockManagementAutoSecurityTimeout = CharacteristicType[int](
    UUID("0000001A-0000-1000-8000-0026BB765291"),
    description="Lock Management Auto Security Timeout",
    format="uint32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="seconds",
)
LockPhysicalControls = CharacteristicType[int](
    UUID("000000A7-0000-1000-8000-0026BB765291"),
    description="Lock Physical Controls",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
LockTargetState = CharacteristicType[int](
    UUID("0000001E-0000-1000-8000-0026BB765291"),
    description="Lock Target State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
Logs = CharacteristicType[bytes](
    UUID("0000001F-0000-1000-8000-0026BB765291"),
    description="Logs",
    format="tlv8",
    permissions=(Permission.PAIRED_READ,),
)
Manufacturer = CharacteristicType[str](
    UUID("00000020-0000-1000-8000-0026BB765291"),
    description="Manufacturer",
    format="string",
    permissions=(Permission.PAIRED_READ,),
)
Model = CharacteristicType[str](
    UUID("00000021-0000-1000-8000-0026BB765291"),
    description="Model",
    format="string",
    permissions=(Permission.PAIRED_READ,),
)
MotionDetected = CharacteristicType[bool](
    UUID("00000022-0000-1000-8000-0026BB765291"),
    description="Motion Detected",
    format="bool",
    permissions=(Permission.PAIRED_READ,),
)
Mute = CharacteristicType[bool](
    UUID("0000011A-0000-1000-8000-0026BB765291"),
    description="Mute",
    format="bool",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
Name = CharacteristicType[str](
    UUID("00000023-0000-1000-8000-0026BB765291"),
    description="Name",
    format="string",
    permissions=(Permission.PAIRED_READ,),
)
NightVision = CharacteristicType[bool](
    UUID("0000011B-0000-1000-8000-0026BB765291"),
    description="Night Vision",
    format="bool",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
NitrogenDioxideDensity = CharacteristicType[float](
    UUID("000000C4-0000-1000-8000-0026BB765291"),
    description="Nitrogen Dioxide Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
ObstructionDetected = CharacteristicType[bool](
    UUID("00000024-0000-1000-8000-0026BB765291"),
    description="Obstruction Detected",
    format="bool",
    permissions=(Permission.PAIRED_READ,),
)
OccupancyDetected = CharacteristicType[int](
    UUID("00000071-0000-1000-8000-0026BB765291"),
    description="Occupancy Detected",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
On = CharacteristicType[bool](
    UUID("00000025-0000-1000-8000-0026BB765291"),
    description="On",
    format="bool",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
OpticalZoom = CharacteristicType[float](
    UUID("0000011C-0000-1000-8000-0026BB765291"),
    description="Optical Zoom",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
OutletInUse = CharacteristicType[bool](
    UUID("00000026-0000-1000-8000-0026BB765291"),
    description="Outlet In Use",
    format="bool",
    permissions=(Permission.PAIRED_READ,),
)
OzoneDensity = CharacteristicType[float](
    UUID("000000C3-0000-1000-8000-0026BB765291"),
    description="Ozone Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
PairSetup = CharacteristicType[bytes](
    UUID("0000004C-0000-1000-8000-0026BB765291"),
    description="Pair Setup",
    format="tlv8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
PairVerify = CharacteristicType[bytes](
    UUID("0000004E-0000-1000-8000-0026BB765291"),
    description="Pair Verify",
    format="tlv8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
PairingFeatures = CharacteristicType[int](
    UUID("0000004F-0000-1000-8000-0026BB765291"),
    description="Pairing Features",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
)
PairingPairings = CharacteristicType[bytes](
    UUID("00000050-0000-1000-8000-0026BB765291"),
    description="Pairing Pairings",
    format="tlv8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
Pm10Density = CharacteristicType[float](
    UUID("000000C7-0000-1000-8000-0026BB765291"),
    description="PM10 Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
Pm2_5Density = CharacteristicType[float](
    UUID("000000C6-0000-1000-8000-0026BB765291"),
    description="PM2.5 Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
PositionState = CharacteristicType[int](
    UUID("00000072-0000-1000-8000-0026BB765291"),
    description="Position State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
ProgramMode = CharacteristicType[int](
    UUID("000000D1-0000-1000-8000-0026BB765291"),
    description="Program Mode",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
ProgrammableSwitchEvent = CharacteristicType[int](
    UUID("00000073-0000-1000-8000-0026BB765291"),
    description="Programmable Switch Event",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2),
)
RelativeHumidityDehumidifierThreshold = CharacteristicType[float](
    UUID("000000C9-0000-1000-8000-0026BB765291"),
    description="Relative Humidity Dehumidifier Threshold",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
RelativeHumidityHumidifierThreshold = CharacteristicType[float](
    UUID("000000CA-0000-1000-8000-0026BB765291"),
    description="Relative Humidity Humidifier Threshold",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
RemainingDuration = CharacteristicType[int](
    UUID("000000D4-0000-1000-8000-0026BB765291"),
    description="Remaining Duration",
    format="uint32",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=3600,
    min_step=1,
)
ResetFilterIndication = CharacteristicType[int](
    UUID("000000AD-0000-1000-8000-0026BB765291"),
    description="Reset Filter Indication",
    format="uint8",
    permissions=(Permission.PAIRED_WRITE,),
    min_value=1,
    max_value=1,
    min_step=1,
)
RotationDirection = CharacteristicType[int](
    UUID("00000028-0000-1000-8000-0026BB765291"),
    description="Rotation Direction",
    format="int32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
RotationSpeed = CharacteristicType[float](
    UUID("00000029-0000-1000-8000-0026BB765291"),
    description="Rotation Speed",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
Saturation = CharacteristicType[float](
    UUID("0000002F-0000-1000-8000-0026BB765291"),
    description="Saturation",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
SecuritySystemAlarmType = CharacteristicType[int](
    UUID("0000008E-0000-1000-8000-0026BB765291"),
    description="Security System Alarm Type",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1,
    min_step=1,
)
SecuritySystemCurrentState = CharacteristicType[int](
    UUID("00000066-0000-1000-8000-0026BB765291"),
    description="Security System Current State",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3, 4),
)
SecuritySystemTargetState = CharacteristicType[int](
    UUID("00000067-0000-1000-8000-0026BB765291"),
    description="Security System Target State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1, 2, 3),
)
SelectedRtpStreamConfiguration = CharacteristicType[bytes](
    UUID("00000117-0000-1000-8000-0026BB765291"),
    description="Selected RTP Stream Configuration",
    format="tlv8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
SerialNumber = CharacteristicType[str](
    UUID("00000030-0000-1000-8000-0026BB765291"),
    description="Serial Number",
    format="string",
    permissions=(Permission.PAIRED_READ,),
    max_length=64,
)
ServiceLabelIndex = CharacteristicType[int](
    UUID("000000CB-0000-1000-8000-0026BB765291"),
    description="Service Label Index",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    min_value=1,
    max_value=255,
    min_step=1,
)
ServiceLabelNamespace = CharacteristicType[int](
    UUID("000000CD-0000-1000-8000-0026BB765291"),
    description="Service Label Namespace",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
SetDuration = CharacteristicType[int](
    UUID("000000D3-0000-1000-8000-0026BB765291"),
    description="Set Duration",
    format="uint32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    min_value=0,
    max_value=3600,
    min_step=1,
)
SetupEndpoints = CharacteristicType[bytes](
    UUID("00000118-0000-1000-8000-0026BB765291"),
    description="Setup Endpoints",
    format="tlv8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
)
SlatType = CharacteristicType[int](
    UUID("000000C0-0000-1000-8000-0026BB765291"),
    description="Slat Type",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
SmokeDetected = CharacteristicType[int](
    UUID("00000076-0000-1000-8000-0026BB765291"),
    description="Smoke Detected",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
StatusActive = CharacteristicType[bool](
    UUID("00000075-0000-1000-8000-0026BB765291"),
    description="Status Active",
    format="bool",
    permissions=(Permission.PAIRED_READ,),
)
StatusFault = CharacteristicType[int](
    UUID("00000077-0000-1000-8000-0026BB765291"),
    description="Status Fault",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
StatusJammed = CharacteristicType[int](
    UUID("00000078-0000-1000-8000-0026BB765291"),
    description="Status Jammed",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
StatusLowBattery = CharacteristicType[int](
    UUID("00000079-0000-1000-8000-0026BB765291"),
    description="Status Low Battery",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
StatusTampered = CharacteristicType[int](
    UUID("0000007A-0000-1000-8000-0026BB765291"),
    description="Status Tampered",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1),
)
StreamingStatus = CharacteristicType[bytes](
    UUID("00000120-0000-1000-8000-0026BB765291"),
    description="Streaming Status",
    format="tlv8",
    permissions=(Permission.PAIRED_READ,),
)
SulphurDioxideDensity = CharacteristicType[float](
    UUID("000000C5-0000-1000-8000-0026BB765291"),
    description="Sulphur Dioxide Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
SupportedAudioStreamConfiguration = CharacteristicType[bytes](
    UUID("00000115-0000-1000-8000-0026BB765291"),
    description="Supported Audio Stream Configuration",
    format="tlv8",
    permissions=(Permission.PAIRED_READ,),
)
SupportedRtpConfiguration = CharacteristicType[bytes](
    UUID("00000116-0000-1000-8000-0026BB765291"),
    description="Supported RTP Configuration",
    format="tlv8",
    permissions=(Permission.PAIRED_READ,),
)
SupportedVideoStreamConfiguration = CharacteristicType[bytes](
    UUID("00000114-0000-1000-8000-0026BB765291"),
    description="Supported Video Stream Configuration",
    format="tlv8",
    permissions=(Permission.PAIRED_READ,),
)
SwingMode = CharacteristicType[int](
    UUID("000000B6-0000-1000-8000-0026BB765291"),
    description="Swing Mode",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
TargetAirPurifierState = CharacteristicType[int](
    UUID("000000A8-0000-1000-8000-0026BB765291"),
    description="Target Air Purifier State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
TargetAirQuality = CharacteristicType[int](
    UUID("000000AE-0000-1000-8000-0026BB765291"),
    description="Target Air Quality",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1, 2),
)
TargetDoorState = CharacteristicType[int](
    UUID("00000032-0000-1000-8000-0026BB765291"),
    description="Target Door State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
TargetFanState = CharacteristicType[int](
    UUID("000000BF-0000-1000-8000-0026BB765291"),
    description="Target Fan State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
TargetHeaterCoolerState = CharacteristicType[int](
    UUID("000000B2-0000-1000-8000-0026BB765291"),
    description="Target Heater Cooler State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1, 2),
)
TargetHeatingCoolingState = CharacteristicType[int](
    UUID("00000033-0000-1000-8000-0026BB765291"),
    description="Target Heating Cooling State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1, 2, 3),
)
TargetHorizontalTiltAngle = CharacteristicType[int](
    UUID("0000007B-0000-1000-8000-0026BB765291"),
    description="Target Horizontal Tilt Angle",
    format="int32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="arcdegrees",
    min_value=-90,
    max_value=90,
    min_step=1,
)
TargetHumidifierDehumidifierState = CharacteristicType[int](
    UUID("000000B4-0000-1000-8000-0026BB765291"),
    description="Target Humidifier Dehumidifier State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1, 2),
)
TargetPosition = CharacteristicType[int](
    UUID("0000007C-0000-1000-8000-0026BB765291"),
    description="Target Position",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
TargetRelativeHumidity = CharacteristicType[float](
    UUID("00000034-0000-1000-8000-0026BB765291"),
    description="Target Relative Humidity",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
TargetSlatState = CharacteristicType[int](
    UUID("000000BE-0000-1000-8000-0026BB765291"),
    description="Target Slat State",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
TargetTemperature = CharacteristicType[float](
    UUID("00000035-0000-1000-8000-0026BB765291"),
    description="Target Temperature",
    format="float",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="celsius",
    min_value=10,
    max_value=38,
    min_step=0.1,
)
TargetTiltAngle = CharacteristicType[int](
    UUID("000000C2-0000-1000-8000-0026BB765291"),
    description="Target Tilt Angle",
    format="int32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="arcdegrees",
    min_value=-90,
    max_value=90,
    min_step=1,
)
TargetVerticalTiltAngle = CharacteristicType[int](
    UUID("0000007D-0000-1000-8000-0026BB765291"),
    description="Target Vertical Tilt Angle",
    format="int32",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="arcdegrees",
    min_value=-90,
    max_value=90,
    min_step=1,
)
TemperatureDisplayUnits = CharacteristicType[int](
    UUID("00000036-0000-1000-8000-0026BB765291"),
    description="Temperature Display Units",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    valid_values=(0, 1),
)
ValveType = CharacteristicType[int](
    UUID("000000D5-0000-1000-8000-0026BB765291"),
    description="Valve Type",
    format="uint8",
    permissions=(Permission.PAIRED_READ,),
    valid_values=(0, 1, 2, 3),
)
Version = CharacteristicType[str](
    UUID("00000037-0000-1000-8000-0026BB765291"),
    description="Version",
    format="string",
    permissions=(Permission.PAIRED_READ,),
    max_length=64,
)
VocDensity = CharacteristicType[float](
    UUID("000000C8-0000-1000-8000-0026BB765291"),
    description="VOC Density",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    min_value=0,
    max_value=1000,
    min_step=1,
)
Volume = CharacteristicType[int](
    UUID("00000119-0000-1000-8000-0026BB765291"),
    description="Volume",
    format="uint8",
    permissions=(Permission.PAIRED_READ, Permission.PAIRED_WRITE),
    unit="percentage",
    min_value=0,
    max_value=100,
    min_step=1,
)
WaterLevel = CharacteristicType[float](
    UUID("000000B5-0000-1000-8000-0026BB765291"),
    description="Water Level",
    format="float",
    permissions=(Permission.PAIRED_READ,),
    unit="percentage",
    min_value=0,
    max_value=100,
)
