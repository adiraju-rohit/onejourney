import sqlite3, uuid, math, os

DB = os.environ.get('DB_PATH', 'nextop.db')

def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

_ic = sqlite3.connect(DB, check_same_thread=False)

_ic.execute('''CREATE TABLE IF NOT EXISTS routes (
    id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    active INTEGER NOT NULL DEFAULT 1
)''')

_ic.execute('''CREATE TABLE IF NOT EXISTS stops (
    id TEXT UNIQUE NOT NULL,
    route_id TEXT NOT NULL,
    name TEXT NOT NULL,
    name_hi TEXT NOT NULL DEFAULT '',
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    sequence INTEGER NOT NULL DEFAULT 0,
    landmark TEXT NOT NULL DEFAULT '',
    landmark_hi TEXT NOT NULL DEFAULT ''
)''')

_ic.commit()
_ic.close()

SEED_ROUTES = [
    ('route_001', 'Route 10H - Secunderabad to Charminar',
     'Secunderabad Station → Tank Bund → Afzalgunj → Charminar'),

    ('route_002', 'Route 218 - Koti to Hitech City',
     'Koti → Lakdikapul → Punjagutta → Madhapur → Hitech City'),

    ('route_003', 'Route 127K - Mehdipatnam to Kondapur',
     'Mehdipatnam → Tolichowki → Gachibowli → Kondapur'),

    ('route_004', 'Route 49M - Dilsukhnagar to Jubilee Hills',
     'Dilsukhnagar → Malakpet → Nampally → Banjara Hills → Jubilee Hills'),

    ('route_005', 'Route 5K - ECIL to Secunderabad',
     'ECIL → Tarnaka → Mettuguda → Secunderabad'),

    ('route_006', 'Route 216 - LB Nagar to Hitech City',
     'LB Nagar → Chaitanyapuri → Ameerpet → Madhapur → Hitech City'),

    ('route_007', 'Route 7Z - Uppal to Gachibowli',
     'Uppal → Habsiguda → Tarnaka → Begumpet → Gachibowli'),

    ('route_008', 'Route 222A - KPHB to Airport',
     'KPHB → JNTU → Miyapur → Gachibowli → Airport'),

    ('route_009', 'Route 113M - Kukatpally to Charminar',
     'Kukatpally → SR Nagar → Lakdikapul → Afzalgunj → Charminar'),

    ('route_010', 'Route 300X - Airport Express',
     'Airport → Aramghar → Mehdipatnam → Lakdikapul → Secunderabad')
]

SEED_STOPS = [

    # Route 10H
    ('route_001', 'Secunderabad Railway Station', 'सिकंदराबाद रेलवे स्टेशन',
     17.4399, 78.4983, 1, 'Main station entrance', 'मुख्य स्टेशन प्रवेश'),

    ('route_001', 'Tank Bund', 'टैंक बंड',
     17.4239, 78.4738, 2, 'Hussain Sagar Lake', 'हुसैन सागर झील'),

    ('route_001', 'Afzalgunj Bus Station', 'अफजलगंज बस स्टेशन',
     17.3734, 78.4747, 3, 'Near Osmania Hospital', 'उस्मानिया अस्पताल के पास'),

    ('route_001', 'Charminar', 'चारमीनार',
     17.3616, 78.4747, 4, 'Historic monument', 'ऐतिहासिक स्मारक'),

    # Route 218
    ('route_002', 'Koti Bus Terminal', 'कोटी बस टर्मिनल',
     17.3850, 78.4867, 1, 'Near Sultan Bazaar', 'सुल्तान बाजार के पास'),

    ('route_002', 'Lakdikapul', 'लकड़ी का पुल',
     17.4045, 78.4626, 2, 'Lakdikapul Junction', 'लकड़ी का पुल जंक्शन'),

    ('route_002', 'Punjagutta', 'पंजागुट्टा',
     17.4295, 78.4483, 3, 'Metro Station', 'मेट्रो स्टेशन'),

    ('route_002', 'Madhapur', 'माधापुर',
     17.4474, 78.3915, 4, 'Cyber Towers Area', 'साइबर टावर्स क्षेत्र'),

    ('route_002', 'Hitech City', 'हाइटेक सिटी',
     17.4435, 78.3772, 5, 'IT Hub', 'आईटी हब'),

    # Route 127K
    ('route_003', 'Mehdipatnam', 'मेहदीपट्टनम',
     17.3995, 78.4390, 1, 'Bus Depot', 'बस डिपो'),

    ('route_003', 'Tolichowki', 'टोलीचौकी',
     17.4038, 78.4124, 2, 'Seven Tombs Road', 'सेवन टॉम्ब्स रोड'),

    ('route_003', 'Gachibowli', 'गाचीबौली',
     17.4401, 78.3489, 3, 'Financial District', 'फाइनेंशियल डिस्ट्रिक्ट'),

    ('route_003', 'Kondapur', 'कोंडापुर',
     17.4698, 78.3638, 4, 'Botanical Garden', 'बॉटनिकल गार्डन'),

    # Route 49M
    ('route_004', 'Dilsukhnagar', 'दिलसुखनगर',
     17.3688, 78.5247, 1, 'Bus Station', 'बस स्टेशन'),

    ('route_004', 'Malakpet', 'मलकपेट',
     17.3731, 78.4900, 2, 'Metro Station', 'मेट्रो स्टेशन'),

    ('route_004', 'Nampally', 'नामपल्ली',
     17.3924, 78.4677, 3, 'Railway Station', 'रेलवे स्टेशन'),

    ('route_004', 'Banjara Hills Road No.1', 'बंजारा हिल्स रोड नं 1',
     17.4189, 78.4382, 4, 'GVK One Mall', 'जीवीके वन मॉल'),

    ('route_004', 'Jubilee Hills Check Post', 'जुबली हिल्स चेक पोस्ट',
     17.4326, 78.4071, 5, 'Metro Station', 'मेट्रो स्टेशन'),

    # Route 5K
    ('route_005', 'ECIL X Roads', 'ईसीआईएल एक्स रोड्स',
     17.4797, 78.5602, 1, 'ECIL Main Junction', 'ईसीआईएल मुख्य जंक्शन'),

    ('route_005', 'Tarnaka', 'तारनाका',
     17.4283, 78.5386, 2, 'OU Entrance', 'ओयू प्रवेश'),

    ('route_005', 'Mettuguda', 'मेट्टुगुडा',
     17.4352, 78.5115, 3, 'Metro Station', 'मेट्रो स्टेशन'),

    ('route_005', 'Secunderabad East', 'सिकंदराबाद पूर्व',
     17.4420, 78.5032, 4, 'Clock Tower Area', 'क्लॉक टावर क्षेत्र'),

    ('route_005', 'Secunderabad Station', 'सिकंदराबाद स्टेशन',
     17.4399, 78.4983, 5, 'Railway Station', 'रेलवे स्टेशन'),

    # Route 216
    ('route_006', 'LB Nagar', 'एलबी नगर',
     17.3457, 78.5522, 1, 'Metro Station', 'मेट्रो स्टेशन'),

    ('route_006', 'Chaitanyapuri', 'चैतन्यपुरी',
     17.3434, 78.5267, 2, 'Metro Corridor', 'मेट्रो कॉरिडोर'),

    ('route_006', 'Dilsukhnagar', 'दिलसुखनगर',
     17.3688, 78.5247, 3, 'Bus Station', 'बस स्टेशन'),

    ('route_006', 'Ameerpet', 'अमीरपेट',
     17.4374, 78.4482, 4, 'Metro Interchange', 'मेट्रो इंटरचेंज'),

    ('route_006', 'Madhapur', 'माधापुर',
     17.4474, 78.3915, 5, 'Cyber Towers', 'साइबर टावर्स'),

    ('route_006', 'Hitech City', 'हाइटेक सिटी',
     17.4435, 78.3772, 6, 'IT Hub', 'आईटी हब'),

    # Route 7Z
    ('route_007', 'Uppal', 'उप्पल',
     17.4018, 78.5591, 1, 'Uppal Metro', 'उप्पल मेट्रो'),

    ('route_007', 'Habsiguda', 'हब्सीगुडा',
     17.4140, 78.5426, 2, 'Street Market', 'स्ट्रीट मार्केट'),

    ('route_007', 'Tarnaka', 'तारनाका',
     17.4283, 78.5386, 3, 'OU Entrance', 'ओयू प्रवेश'),

    ('route_007', 'Begumpet', 'बेगमपेट',
     17.4440, 78.4625, 4, 'Airport Road', 'एयरपोर्ट रोड'),

    ('route_007', 'Madhapur', 'माधापुर',
     17.4474, 78.3915, 5, 'Cyber Towers', 'साइबर टावर्स'),

    ('route_007', 'Gachibowli', 'गाचीबौली',
     17.4401, 78.3489, 6, 'Financial District', 'फाइनेंशियल डिस्ट्रिक्ट'),

    # Route 222A
    ('route_008', 'KPHB Colony', 'केपीएचबी कॉलोनी',
     17.4931, 78.3991, 1, 'Forum Mall', 'फोरम मॉल'),

    ('route_008', 'JNTU', 'जेएनटीयू',
     17.4938, 78.3912, 2, 'University Gate', 'विश्वविद्यालय द्वार'),

    ('route_008', 'Miyapur', 'मियापुर',
     17.4967, 78.3572, 3, 'Metro Station', 'मेट्रो स्टेशन'),

    ('route_008', 'Gachibowli', 'गाचीबौली',
     17.4401, 78.3489, 4, 'Financial District', 'फाइनेंशियल डिस्ट्रिक्ट'),

    ('route_008', 'RGIA Airport', 'आरजीआईए एयरपोर्ट',
     17.2403, 78.4294, 5, 'Terminal Building', 'टर्मिनल भवन'),

    # Route 113M
    ('route_009', 'Kukatpally', 'कुकटपल्ली',
     17.4849, 78.4138, 1, 'Bus Depot', 'बस डिपो'),

    ('route_009', 'SR Nagar', 'एसआर नगर',
     17.4418, 78.4450, 2, 'Metro Station', 'मेट्रो स्टेशन'),

    ('route_009', 'Lakdikapul', 'लकड़ी का पुल',
     17.4045, 78.4626, 3, 'Junction', 'जंक्शन'),

    ('route_009', 'Afzalgunj', 'अफजलगंज',
     17.3734, 78.4747, 4, 'Bus Station', 'बस स्टेशन'),

    ('route_009', 'Charminar', 'चारमीनार',
     17.3616, 78.4747, 5, 'Historic Monument', 'ऐतिहासिक स्मारक'),

    # Route 300X Airport Express
    ('route_010', 'RGIA Airport', 'आरजीआईए एयरपोर्ट',
     17.2403, 78.4294, 1, 'Terminal Building', 'टर्मिनल भवन'),

    ('route_010', 'Aramghar', 'आरामघर',
     17.3395, 78.4290, 2, 'PVNR Expressway', 'पीवीएनआर एक्सप्रेसवे'),

    ('route_010', 'Mehdipatnam', 'मेहदीपट्टनम',
     17.3995, 78.4390, 3, 'Bus Depot', 'बस डिपो'),

    ('route_010', 'Lakdikapul', 'लकड़ी का पुल',
     17.4045, 78.4626, 4, 'Junction', 'जंक्शन'),

    ('route_010', 'Begumpet', 'बेगमपेट',
     17.4440, 78.4625, 5, 'Airport Road', 'एयरपोर्ट रोड'),

    ('route_010', 'Secunderabad Station', 'सिकंदराबाद स्टेशन',
     17.4399, 78.4983, 6, 'Railway Station', 'रेलवे स्टेशन'),
]

def seed():
    conn = get_conn()
    for rid, name, desc in SEED_ROUTES:
        if not conn.execute("SELECT id FROM routes WHERE id=?", (rid,)).fetchone():
            conn.execute("INSERT INTO routes(id,name,description,active) VALUES(?,?,?,1)",
                         (rid, name, desc))
    for row in SEED_STOPS:
        rid, name, name_hi, lat, lng, seq, lm, lm_hi = row
        sid = f"stop_{rid}_{seq}"
        if not conn.execute("SELECT id FROM stops WHERE id=?", (sid,)).fetchone():
            conn.execute("INSERT INTO stops(id,route_id,name,name_hi,lat,lng,sequence,landmark,landmark_hi) VALUES(?,?,?,?,?,?,?,?,?)",
                         (sid, rid, name, name_hi, lat, lng, seq, lm, lm_hi))
    conn.commit()
    conn.close()

seed()

def haversine(lat1, lng1, lat2, lng2):
    """Returns distance in kilometers between two lat/lng points."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_all_routes():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM routes WHERE active=1 ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_route(route_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM routes WHERE id=?", (route_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}

def get_stops(route_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM stops WHERE route_id=? ORDER BY sequence ASC", (route_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_stops():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM stops ORDER BY route_id, sequence").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def find_next_stop(route_id, lat, lng, threshold_km=1.0):
    """Given current location, find the nearest upcoming stop within threshold_km."""
    stops = get_stops(route_id)
    closest = None
    closest_dist = float('inf')
    for stop in stops:
        dist = haversine(lat, lng, stop['lat'], stop['lng'])
        if dist <= threshold_km and dist < closest_dist:
            closest_dist = dist
            closest = stop
    return closest, closest_dist if closest else (None, None)

def get_nearby_stops(lat, lng, route_id, threshold_km=1.0):
    """Return all stops on route within threshold_km, sorted by distance."""
    stops = get_stops(route_id)
    result = []
    for stop in stops:
        dist = haversine(lat, lng, stop['lat'], stop['lng'])
        result.append({**stop, 'distance_km': round(dist, 3)})
    result.sort(key=lambda x: x['distance_km'])
    nearby = [s for s in result if s['distance_km'] <= threshold_km]
    return nearby

def add_route(name, description):
    conn = get_conn()
    rid = 'route_' + str(uuid.uuid4())[:8]
    conn.execute("INSERT INTO routes(id,name,description,active) VALUES(?,?,?,1)", (rid, name, description))
    conn.commit()
    conn.close()
    return rid

def add_stop(route_id, name, name_hi, lat, lng, sequence, landmark='', landmark_hi=''):
    conn = get_conn()
    sid = 'stop_' + str(uuid.uuid4())[:8]
    conn.execute("INSERT INTO stops(id,route_id,name,name_hi,lat,lng,sequence,landmark,landmark_hi) VALUES(?,?,?,?,?,?,?,?,?)",
                 (sid, route_id, name, name_hi, lat, lng, sequence, landmark, landmark_hi))
    conn.commit()
    conn.close()
    return sid

def delete_stop(stop_id):
    conn = get_conn()
    conn.execute("DELETE FROM stops WHERE id=?", (stop_id,))
    conn.commit()
    conn.close()

def delete_route(route_id):
    conn = get_conn()
    conn.execute("DELETE FROM stops WHERE route_id=?", (route_id,))
    conn.execute("DELETE FROM routes WHERE id=?", (route_id,))
    conn.commit()
    conn.close()
