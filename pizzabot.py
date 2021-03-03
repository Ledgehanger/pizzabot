import argparse
import re

pizza_parse = argparse.ArgumentParser(prog="pizzabot",
                                      usage="pizzabot 'grid_size (coords_for_delivery)'",
                                      description="Helps Pizzabot find the best route to deliver pizza quickly and "
                                                  "efficiently")
pizza_parse.add_argument('delivery_string',
                         type=str)


def pizzabot(delivery_string):
    # We need to split the string to allow us to build our grid and get
    # coordinates. Regex is used here to ensure that we always get the correct elements
    input_list = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', delivery_string)

    # Lets put the grid size for the x and y axis into there own variable,
    # convert to ints and remove from list
    x_grid_size, y_grid_size = input_list[0].split('x')
    x_grid_size = int(x_grid_size)
    y_grid_size = int(y_grid_size)
    input_list.pop(0)

    # If the grid size is less than or equal to 0x0, bomb out since its an invalid grid
    if x_grid_size <= 0 and y_grid_size <= 0:
        raise Exception(f"Cannot create grid of size {x_grid_size}x{y_grid_size}."
                        "Please create a grid size greater than 0x0 to create a valid "
                        "grid")

    # Set start positioning for pizzabot
    x_curr_pos = 0
    y_curr_pos = 0
    pizzabot_path = ""

    # Lets go over the list of coordinates and deliver the pizza for pizzabot
    for destination in input_list:
        dest = destination.replace('(', '')
        dest = dest.replace(')', '')
        dest_x, dest_y = dest.split(', ')
        dest_x = int(dest_x)
        dest_y = int(dest_y)

        if dest_x > x_grid_size:
            raise Exception(f"X Coordinate {dest_x} is greater than grid size {x_grid_size}."
                            f" Enter in a grid size less than {x_grid_size}")
        if dest_y > y_grid_size:
            raise Exception(f"Y Coordinate {dest_y} is greater than grid size {y_grid_size}."
                            f" Enter in a grid size less than {y_grid_size}")

        # Now that we have got our values, done some exception handling, lets gets started
        # If the x_curr_pos is less than dest_x, we know are going right, so take away dest_x
        # from x_curr_pos, add that number of E and update our current x_curr_pos to dest_x
        if x_curr_pos < dest_x:
            pizzabot_path = f"{pizzabot_path}{'E' * (dest_x - x_curr_pos)}"
            x_curr_pos = dest_x
        else:
            pizzabot_path = f"{pizzabot_path}{'W' * (x_curr_pos - dest_x)}"
            x_curr_pos = dest_x

        if y_curr_pos < dest_y:
            pizzabot_path = f"{pizzabot_path}{'N' * (dest_y - y_curr_pos)}"
            y_curr_pos = dest_y

        else:
            pizzabot_path = f"{pizzabot_path}{'S' * (y_curr_pos - dest_y)}"
            y_curr_pos = dest_y

        pizzabot_path = f"{pizzabot_path}D"

    print(pizzabot_path)


if __name__ == "__main__":
    pizzabot(pizza_parse.parse_args().delivery_string)
