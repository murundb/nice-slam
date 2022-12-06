import os
import sys
import click

import numpy as np

def get_matrix_from_quaternion(quaternion):
    q_w = quaternion[0]
    q_x = quaternion[1]
    q_y = quaternion[2]
    q_z = quaternion[3]

    # Refer to Groves p41

    R_00 = 1.0 - 2.0 * (q_y**2 + q_z**2)
    R_01 = 2.0 * (q_x * q_y - q_z * q_w)
    R_02 = 2.0 * (q_x * q_z + q_y * q_w)
    R_10 = 2.0 * (q_x * q_y + q_z * q_w)
    R_11 = 1.0 - 2.0 * (q_x**2 + q_z**2)
    R_12 = 2.0 * (q_y * q_z - q_x * q_w)
    R_20 = 2.0 * (q_x * q_z - q_y * q_w)
    R_21 = 2.0 * (q_y * q_z + q_x * q_w)
    R_22 = 1.0 - 2.0 * (q_x**2 + q_y**2)

    R_from_quaternion = np.array([
        [R_00, R_01, R_02],
        [R_10, R_11, R_12],
        [R_20, R_21, R_22]
    ])

    return R_from_quaternion

def convert_pose(input_file, output_dir):
    
    with open(input_file, "r") as f:
        lines = f.readlines()
        pose_count = 0

        for line in lines:
            filename = str(pose_count) + ".txt"
            output_file = os.path.join(output_dir, filename)
            data = line.strip().split()

            timestamp = data[0]
            t_world_world_body_meters = np.array([float(data[1]), float(data[2]), float(data[3]), 1.0])
            quaternion = np.array([float(data[4]), float(data[5]), float(data[6]), float(data[7])])

            R_world_from_body = get_matrix_from_quaternion(quaternion)

            T_world_from_body = np.zeros((4, 4), dtype=np.float)
            T_world_from_body[:3, :3] = R_world_from_body
            T_world_from_body[:, 3] = t_world_world_body_meters

            np.savetxt(output_file, T_world_from_body, fmt='%.6f', delimiter=' ')

            pose_count += 1
    


@click.command()
@click.option("--input-file", "-i", required=True, type=str, help="Input pose to convert")
@click.option("--output-dir", "-o", required=False, type=str, help="Output directory to write the converted pose")
def main(input_file, output_dir="conversion_temp"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(input_file):
        sys.exit("Input file doesn't exist")
    
    convert_pose(input_file, output_dir)

if __name__ == "__main__":
    main()