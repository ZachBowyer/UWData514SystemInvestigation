# Data description
The General Transit Feed Specification (GTFS) is a static public transit dataset.  
(Real time data is available via API).   
This dataset only contains the publicly available static data related to Trimet.   
Dataset homepage: http://developer.trimet.org/GTFS.shtml  
File come as gtfs.zip
Each file in the unzipped is a .txt file that is separated by commas (It's csv)  
Number of rows was original download, subject to change. 
This is real time data periodically updated
Offical dataset documentation here: https://developers.google.com/transit/gtfs/reference#term_definitions
Directions for dataset from instructor: https://drive.google.com/drive/folders/1R9AcwnJ8-DUfKevTnCjHsTiTUnwqT5Hl  

# Gtfs.zip contains:  
## Format: File name; size; number of rows; 12; used in project (3 spaces between)
    Agency.txt;             1kb;        3 rows;         Used
    calendar.txt;           2kb;        56 rows;        Used
    calendar_dates.txt;     10kb;       598 rows;       Used
    fare_attributes.txt;    1kb;        7 rows;         Used
    fare_rules.txt;         1kb;        12 rows;        Used
    feed_info.txt;          1kb;        1 row;          Not used
    linked_datasets.txt;    1kb;        3 rows;         Not used
    route_directions.txt;   6kb;        184 rows;       Used
    routes.txt;             8kb;        94 rows;        Used
    shapes.txt;             27645kb;    989919 rows;    Used
    stop_features.txt;      937kb;      39393 rows;     Used
    stop_times.txt;         156879kb;   3046657 rows;   Used
    stops.txt;              1159kb;     6558 rows;      Used
    transfers.txt;          49kb;       3730 rows;      Used
    trips.txt;              1780kb;     64647 rows;     USed

# File descriptions
## Format: Name of file, size, number of rows. Below that is attribute, data type, example
## agency.txt; 1kb; 3 Rows
    agency_id;          string;   "TRIMET"  
    agency_name;        string;   "TriMet"  
    agency_url;         string;   "https://trimet.org/"  
    agency_timezone;    string;   "America/Los_Angeles"  
    agency_lang;        string;   "en"  
    agency_phone;       string;   "503-238-RIDE"  
    agency_fare_url;    string;   "https://trimet.org/fares/"  
    agency_email;       string;   "customerservice@trimet.org"  
    bikes_policy_url;   string;   "https://trimet.org/bikes/bikepolicies.htm"  

# calendar.txt; 2kb; 56 rows
    service_id;   string;    "C.645"
    monday;       integer;   0
    tuesday;      integer;   0
    wednesday;    integer;   0
    thursday;     integer;   0
    friday;       integer;   0
    saturday;     integer;   0
    sunday;       integer;   0
    start_date;   integer;   20230416 
    end_date;     integer;   20230429

# calendar_dates.txt; 10kb; 598 rows
    service_id;       string;    "B.647"
    date;             integer;   20230513
    exception_type;   integer;   1

# fare_attributes.txt; 1kb; 7 rows
    fare_id;             string;    "B"
    agency_id;           string;    "TRIMET"
    price;               float;     2.5
    currency_type;       string;    "USD"
    payment_method;      integer;   0
    transfers;           integer;   0
    transfer_duration;   integer;   9000

# fare_rules.txt; 1kb; 12 rows
    fare_id;       string;    "B"
    origin_id;     string;    "B"
    route_id;      integer;   98
    contains_id;   string;    "R"

# feed_info.txt; 1kb; 1 row
    feed_publisher_name;   string;    "Trimet"
    feed_publisher_url;    string;    "https://trimet.org/"
    feed_lang;             string;    "en"
    feed_start_date;       integer;   20230430
    feed_end_date;         integer;   20230826
    feed_version;          string;    "20230430-20230510-1500"
    feed_id;               string;    "TriMet"
    feed_contact_url;      string;    "https://groups.google.com/forum/#!forum/transit-developers-pdx"

# linked_datasets.txt; 1kb; 3 rows
    url;                       string;    "http://developer.trimet.org/ws/V1/TripUpdate"
    trip_updates;              integer;   1
    vehicle_positions;         integer;   0
    service_alerts;            integer;   0
    authentication_type;       integer;   2
    authentication_info_url;   string;    "https://developer.trimet.org/GTFS.shtml"
    api_key_parameter_name;    string;    "appID"

# route_directions.txt; 6kb; 184 rows
    route_id;         integer;   1
    direction_id;     integer;   0
    direction_name;   string;    "To Vermont & Shattuck and Maplewood"

# routes.txt; 8kb; 94 rows
    route_id;           integer;   1
    agency_id;          string;    "TRIMET"
    route_short_name;   string;    "1"
    route_long_name;    string;    "Vermont"
    route_type;         integer;   3
    route_url;          string;    "https://trimet.org/schedules/r001.htm"
    route_color;        string;    "61A60E"
    route_text_color;   string;    "FFFFFF"
    route_sort_order;   integer;   7000

# shapes.txt; 27645kb; 989919 rows
    shape_id;              integer;   535813
    shape_pt_lat;          float;     45.522879
    shape_pt_lon;          float;     -122.677396
    shape_pt_sequence;     integer;   1
    shape_dist_traveled;   float;     12.6

# stop_features.txt; 937kb; 39393 rows
    stop_id;        integer;   2
    feature_name;   string;    "Pavement at back door"

# stop_times.txt; 156879kb; 3047657 rows
    trip_id;               integer;   12336459
    arrival_time;          string;    "15:10:00"
    departure_time;        string;    "15:10:00"
    stop_id;               integer;   13170
    stop_sequence;         integer;   1
    stop_headsign;         string;    "Vermont Shattuck Loop via Maplewood"
    pickup_type;           integer;   0
    drop_off_type;         integer;   1
    shape_dist_traveled;   float;     0.0
    timepoint;             integer;   1
    continuous_drop_off;   string;    "null" (Data nonexistent)
    continuous_pickup;     string;    "null" (Data nonexistent)

# stops.txt; 1159kb; 6558 rows
    stop_id;          integer;   2
    stop_code;        integer;   2
    stop_name;        string;    "A Ave & Chandler"
    tts_stop_name;    string;    "ae avenue & chandler"
    stop_desc;        string;    "Eastbound stop in Lake Oswego (Stop ID 2)"
    stop_lat;         float;     45.420609
    stop_lon;         float;     -122.675671
    zone_id;          string;    "B"
    stop_url;         string;    "https://trimet.org/home/stop/2"
    location_type;    integer;   0
    parent_station;   string;    "null" (Data nonexistent)
    direction;        string;    "East"
    position;         string;    "Nearside"

# transfers.txt; 49kb; 3730 rows
    from_stop_id;    integer;   46
    to_stop_id;      integer;   5889
    transfer_type;   integer;   0

# trips.txt; 1780kb; 64647 rows
    route_id;                integer;   1
    service_id;              string;    "W.647"
    trip_id;                 integer;   12336459
    trip_short_name;         string;    "null" (Data nonexistent)
    direction_id;            integer;   0
    block_id;                integer;   6174
    shape_id;                integer;   534051
    trip_type;               string;    "null" (data nonexistent)
    wheelchair_accessible;   integer;   1