robot_art = r"""
      0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}                              
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|          
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/        
      | ||        || |          |4: {left_leg_name} 
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}
                                
"""

print(robot_art)


class Part():
    def __init__(self, name: str, attack_level=0, defense_level=0, energy_consumption=0):
        self.name = name
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.energy_consumption = energy_consumption

    def get_status_dict(self):
        formatted_name = self.name.replace(" ", "_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(),
            "{}_status".format(formatted_name): self.is_available(),
            "{}_attack".format(formatted_name): self.attack_level,
            "{}_defense".format(formatted_name): self.defense_level,
            "{}_energy_consump".format(formatted_name): self.energy_consumption,
        }

    def is_available(self):
        return not self.defense_level <= 0


colors = {
    "Black": '\x1b[90m',
    "Red": '\x1b[91m',
    "Green": '\x1b[92m',
    "Yellow": '\x1b[93m',
    "Blue": '\x1b[94m',
    "Magenta": '\x1b[95m',
    "Cyan": '\x1b[96m',
    "White": '\x1b[97m',
    "Reset": '\x1b[0m',
}


class Robot:
    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code
        self.energy = 100
        self.parts = [
            Part("Head", attack_level=5, defense_level=10, energy_consumption=5),
            Part("Weapon", attack_level=15,
                 defense_level=0, energy_consumption=10),
            Part("Left Arm", attack_level=3,
                 defense_level=28, energy_consumption=10),
            Part("Right Arm", attack_level=6,
                 defense_level=28, energy_consumption=10),
            Part("Left Leg", attack_level=4,
                 defense_level=28, energy_consumption=15),
            Part("Right Leg", attack_level=8,
                 defense_level=20, energy_consumption=15),
        ]

    def greet(self):
        print("Hello, my name is", self.name)

    # def print_energy(self):
    #     print("We have", self.energy, "percent energy left")

    def print_energy(self):
        print("Energy bar:")
        for i in range(0, self.energy):
            print("=", end="", )
        print("")
        print("We have", self.energy, "percent energy left")

    def attack(self, enemy_robot, part_to_use, part_to_attack):
        enemy_robot.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level
        self.energy -= self.parts[part_to_use].energy_consumption

    def is_on(self):
        return self.energy >= 0

    def is_there_available_parts(self):
        for part in self.parts:
            if part.is_available():
                return True
            return False

    def print_status(self):
        print(self.color_code)
        str_robot = robot_art.format(**self.get_part_status())
        self.greet()
        self.print_energy()
        print(str_robot)
        print(colors["Black"])

    def get_part_status(self):
        part_status = {}
        for part in self.parts:
            status_dict = part.get_status_dict()
            part_status.update(status_dict)
        return part_status


def build_robot():
    print("****************************")
    print("**                        **")
    print("**  welcome to the game   **")
    print("**                        **")
    print("****************************")
    robot_name = input("Robot name: ")
    color_code = choose_color()
    robot = Robot(robot_name, color_code)
    robot.print_status()
    return robot


def choose_color():
    print("Choose a color for your robot:")
    for color in colors.keys():
        print(color)
    color = input("Color: ")
    return colors[color]


def choose_part(robot):
    print("Choose a part to use:")
    for index, part in enumerate(robot.parts):
        if part.is_available():
            print(index, part.name)
    part = int(input("Part: "))
    return part


def choose_part_to_attack(robot):
    print("Choose a part to attack:")
    for index, part in enumerate(robot.parts):
        if part.is_available():
            print(index, part.name)
    part = int(input("Part: "))
    return part


def main():

    robot1 = build_robot()
    robot2 = build_robot()
    while robot1.is_on() and robot2.is_on() and robot1.is_there_available_parts() and robot2.is_there_available_parts():
        robot1.print_status()
        robot2.print_status()
        part_to_use = choose_part(robot1)
        part_to_attack = choose_part_to_attack(robot2)
        robot1.attack(robot2, part_to_use, part_to_attack)
        robot1, robot2 = robot2, robot1
    robot1.print_status()
    robot2.print_status()
    if robot1.is_on() and robot1.is_there_available_parts():
        print("****************************")
        print(robot1.name, "is won!")
        print("****************************")
    elif robot2.is_on() and robot2.is_there_available_parts():
        print("****************************")
        print(robot2.name, "is won!")
        print("****************************")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
