#! /usr/bin/env python3
from owlready2 import *
import random
import os
import glob

import rospy
import std_msgs.msg as std
from service_node.srv import GetSemDist, GetSemDistResponse

onto = get_ontology('/home/mike/catkin_ws/src/recognition/src/Recognition_from_Ontology/Ontology/Genova_streets.owl')
onto.load()
all_classes=list(onto.classes())



def get_dist(class1,class2):
    anc1=[]
    anc2=[]
    fath1=class1
    fath2=class2
    common_fa=None
    while fath1.is_a:
        anc1.append(fath1)
        fath1=fath1.is_a[0]
    while fath2.is_a:
        anc2.append(fath2)
        fath2=fath2.is_a[0]
    for each1 in anc1:
        for each2 in anc2:
            if each1==each2:
                common_fa=each1
                break
        else:
            continue

        break
    if common_fa:
        return anc1.index(common_fa)+anc2.index(common_fa)
    else:
        return False    


def handle_sem_dist(req):
    ind1=req.a
    ind2=req.b
    

    class1=all_classes[ind1]
    
    class2=all_classes[ind2]

    print("WORDS With a new added link " + class1.name + " " + class2.name)
    
    dist=get_dist(class1,class2)
    #print("before result ",dist)
    # if dist:
    #     GetSemDistResponse(dist)
    #     return True
    return GetSemDistResponse(dist)

def get_sem_dist_server():
    rospy.init_node('get_sem_dist_server')


    s = rospy.Service('get_sem_dist', GetSemDist, handle_sem_dist)
    print("ready to give sem distance")
    rospy.spin()




if __name__=="__main__":
    #print(os.getcwd())
    
    get_sem_dist_server()