import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from datetime import datetime

# Define the TemperatureLogger node
class TemperatureLogger(Node):
    def __init__(self, filename):
        super().__init__("temperature_logger")
        self.filename = filename
        self.subscription = self.create_subscription(
            Float32, "/temperature", self.callback, 10)
        
    def callback(self, msg):
        temperature = msg.data
        if temperature >= 50.0:
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"{time_str} - {temperature:.2f} C"
            self.get_logger().warn(line)
            try:
                with open(self.filename, "a") as f:
                    f.write(line + "\n")
            except OSError as error:
                self.get_logger().error(f"Could not write to log file: {error}")


def main(args=None):
    rclpy.init(args=args)

    logger = TemperatureLogger("log.txt")

    rclpy.spin(logger)

    logger.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
