class TheWayFormatter:

    def lists_creator(self, data_dict: dict, flight_names: list, flight_waypoints: list):

        for n in data_dict['Mission']['Routes']['Route']:
            flight_names.append(n['Name'])
            waypoint_num = 0
            each_flight_waypoints = []
            for x in n['Waypoints']['Waypoint']:
                lat = x['Lat']
                lon = x['Lon']
                elev = float(x['Altitude']) * 0.3048
                waypoint_num += 1
                waypoint_dict = {
                    "id": waypoint_num,
                    "name": f"Waypoint {waypoint_num}",
                    "lat": lat,
                    "long": lon,
                    "elev": elev
                }
                each_flight_waypoints.append(waypoint_dict)
            flight_waypoints.append(each_flight_waypoints)

    def file_writer(self, flight_names: list, flight_waypoints: list):

        for n in range(len(flight_names)):
            with open(f"TW_Files/{flight_names[n]}.tw", mode='w') as file:
                waypoint_string = str(flight_waypoints[n])
                joined = waypoint_string.replace(" ", "")
                apostrophe_replaced = joined.replace("'", '"')
                file.write(f"{apostrophe_replaced}")
