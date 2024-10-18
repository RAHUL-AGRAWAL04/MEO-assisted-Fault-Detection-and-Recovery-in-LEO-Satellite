def modify_tle_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    
    modified_tle = []
    satellite_count = 0
    tle_chunk_size = 3  

    for i in range(0, len(lines), tle_chunk_size):
        if i + 2 >= len(lines):
            break  
        
        tle_name = lines[i].strip()  
        tle_line1 = lines[i+1].strip()  
        tle_line2 = lines[i+2].strip()  

        satellite_count += 1
        modified_name = f"{tle_name} {satellite_count-1}"
        modified_tle.append(modified_name)
        modified_tle.append(tle_line1)
        modified_tle.append(tle_line2)
    output_lines = [f"{satellite_count}"] + modified_tle

    with open(output_filename, 'w') as outfile:
        outfile.write("\n".join(output_lines) + "\n")

    print(f"Modified TLE file saved to {output_filename}")

input_tle_file = 'Input/data/ONEWEB-tle.txt'  
output_tle_file = 'output/ONEWEB_annotted.txt' 

modify_tle_file(input_tle_file, output_tle_file)
