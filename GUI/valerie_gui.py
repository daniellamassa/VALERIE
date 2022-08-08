#!/usr/bin/env python3
import rospy,math
from std_msgs.msg import String
from geometry_msgs.msg import Twist

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivy.metrics import dp


speech_list = ["[size=30]Hi, my name is Valerie!", "[size=30]What can I help you with today?", "[size=30]Can you give me directions to ISEC?", "[size=30]Would you like to learn about research on campus?", "[size=30]It was nice talking to you!", "[size=30]Goodbye."]

class ValerieApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen=Builder.load_file('/home/massad/Desktop/kivy_stuff/valerie/gui.kv')

        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(45),
                "on_release": lambda x = f"{i}": self.menu_callback(x),
            } for i in speech_list
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.button,
            items=menu_items,
            position="bottom",
            width_mult=6.5,
            max_height=dp(280),
        )

    def menu_callback(self, text_item):
        print(text_item)

    def build(self):
        return self.screen


    def move(self,distance, isForward):
        move_publish = rospy.Publisher("/cmd_vel",Twist, queue_size=10)
        outData = Twist()
        t0 = rospy.get_rostime().secs
        while t0 == 0:
            t0 = rospy.get_rostime().secs
        current_distance = 0
        rate = rospy.Rate(5)
        if isForward == True:
           outData.linear.x = 0.2
        else:
           outData.linear.x = -0.2
        while current_distance < distance:
            move_publish.publish(outData)
            t1 = rospy.get_rostime().secs
            current_distance = abs(outData.linear.x * (t1 - t0))
            rate.sleep()


    def rotate(self,relative_angle, isClockwise):
        rotate_publish = rospy.Publisher("/cmd_vel",Twist, queue_size=10)
        outData = Twist()
        t0 = rospy.get_rostime().secs
        while t0 == 0:
            t0 = rospy.get_rostime().secs
        current_angle = 0
        rate = rospy.Rate(5)
        if isClockwise == True:
           outData.angular.z = 30.0
        else:
           outData.angular.z = -30.0

        while abs(current_angle) < abs(relative_angle):
            rotate_publish.publish(outData)
            t1 = rospy.get_rostime().secs
            current_angle = abs(outData.angular.z * (t1 - t0))
            rate.sleep()

    def expression_display(self,outData):
        face_publish = rospy.Publisher("/face_listener",String, queue_size=10)
        face_publish.publish(outData)

if __name__ == '__main__':
    rospy.init_node('simple_gui', anonymous=True)
    ValerieApp().run()
