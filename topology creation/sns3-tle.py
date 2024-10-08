def modify_tle_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
    
    modified_tle = []
    satellite_count = 0
    tle_chunk_size = 3  # Each TLE consists of 3 lines

    # Loop over the file in chunks of 3 lines (1 satellite = 3 lines)
    for i in range(0, len(lines), tle_chunk_size):
        if i + 2 >= len(lines):
            break  # Ensure we do not go out of bounds
        
        # Extract the 3-line TLE for a satellite
        tle_name = lines[i].strip()  # First line (name)
        tle_line1 = lines[i+1].strip()  # Second line
        tle_line2 = lines[i+2].strip()  # Third line

        # Increment satellite count
        satellite_count += 1

        # Modify the first line to include "Name Number N"
        modified_name = f"{tle_name} Number {satellite_count}"

        # Append the modified TLE to the list
        modified_tle.append(modified_name)
        modified_tle.append(tle_line1)
        modified_tle.append(tle_line2)

    # Add the total satellite count as the first line in the output
    output_lines = [f"Total Satellites: {satellite_count}"] + modified_tle

    # Write the modified TLE to the output file
    with open(output_filename, 'w') as outfile:
        outfile.write("\n".join(output_lines) + "\n")

    print(f"Modified TLE file saved to {output_filename}")

# Example usage
input_tle_file = 'input_tle.txt'  # Input file containing the original TLE data
output_tle_file = 'output_tle.txt'  # Output file for modified TLE data

modify_tle_file(input_tle_file, output_tle_file)
