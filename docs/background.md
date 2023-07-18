# Localization and Monitoring Using Passive RF on the Internet-of-Things
By **Kacey La**\
Advised by **Dr. Mongan** and **Dr. Christopher Tralie** \
<code>**Ursinus College** - **Summer Fellows**</code>

>**Presentations:** \
> Week 2 - <a href="slides/Week2_Densepose.pdf" download>Slides</a>\
> Week 4 - <a href="slides/Week4_Densepose.pdf" download>Slides</a>\
> Week 6 - <a href="slides/Week6_Densepose.pdf" download>Slides</a>

## Abstract

In remote healthcare monitoring, devices such as RGB cameras and radar are used to monitor patient activity. However, these devices have several disadvantages. The effectiveness of RGB cameras is dependent on the lighting, and poses privacy concerns. Radar, on the other hand, can be unaffordable to many households due to its price and high power-consumption. To address these limitations, this project explores WiFi signals as a solution using commercial off-the-shelf routers. WiFi signals have the benefit of working effectively regardless of lighting conditions and can even protect privacy by stripping away patient visual information. Through monitoring the changes in signal reflections caused by the WiFi signal bouncing off of people and objects in a room, the patient's activity can be inferred. The phase and amplitude of the WiFi signals, known as the channel state information (CSI) are collected and used in a Densepose neutral network which estimates the pose of the patient by outputting a 2D representation of the 3D human geometry called UV coordinates.


&nbsp;  