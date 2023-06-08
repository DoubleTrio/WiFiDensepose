#!/bin/sh

##################################################################################
# NOTE - This is script is modified from https://openwrt.org/docs/guide-user/hardware/led/wifi.meter
##################################################################################

#Filename: ledwsignal.sh 
#Description: This script shows wifi signal strength by blinking one led.
#2015 raphik, danitool

EXTENSION=`echo "$1" | cut -d'.' -f2`

if [ "$EXTENSION" != "csv" ];
  printf "\nUSAGE:
  rssi.sh <*.csv>
  \n\nERROR\n"
  exit 255
fi;

Led_On() { 
	echo $2 > /sys/class/leds/$1/delay_on 
}
 
Led_Off() {
	echo $2 > /sys/class/leds/$1/delay_off
}

Get_Strength() {
  if [ -z $1 ] || [ $1 -ge 0 ]; then echo 0 #error
  elif [ $1 -ge -65 ] ; then echo 4 #excellent
  elif [ $1 -ge -73 ] ; then echo 3 #good
  elif [ $1 -ge -80 ] ; then echo 2 #fair
  elif [ $1 -ge -94 ] ; then echo 1 #bad
  else echo 0
  fi
}

Trigger_LED() {
  # $1 - measured strength
  # $2 - old strength
  # $3 - LED
  # $4 - antinne number
  # $5 - measured RSSI
  if [ $2 = 4 ] ; then echo timer > /sys/class/leds/$3/trigger
  fi
  case $1 in
    4)  Led_On $3 1960; Led_Off $3 40 ;;
    3)  Led_On $3 950;  Led_Off $3 50  ;;
    2)  Led_On $3 500;  Led_Off $3 500 ;;
    1)  Led_On $3 50;   Led_Off $3 950  ;;
    0)  Led_On $3 40;   Led_Off $3 1960 ;; 
  esac
  echo "#$4 SIGNAL STRENGTH (RSSI: $5) (0-4): $1"
}

OLD_STRENGTH1=-1
OLD_STRENGTH2=-1
OLD_STRENGTH3=-1

LED1="green:lan1"
LED2="green:lan2"
LED3="green:lan3"

echo timer > /sys/class/leds/$LED1/trigger
echo timer > /sys/class/leds/$LED2/trigger
echo timer > /sys/class/leds/$LED3/trigger

while true ; do
  DUMP=`iw dev wlan0 station dump`
  TIMESTAMPNSEC=`echo "$DUMP" | tail -1 |  awk '{ print $3 }'`
  SIGNALS=`echo "$DUMP" | grep "signal:" | grep -o '\[.*]' | sed 's/\[//g' | sed 's/]//g' | sed 's/[[:space:]]*//g'`
  echo $TIMESTAMPNSEC
  RSSI1=`echo $SIGNALS | cut -d',' -f1`
  RSSI2=`echo $SIGNALS | cut -d',' -f2`
  RSSI3=`echo $SIGNALS | cut -d',' -f3`

  if [ -z "$RSSI1" ] ;
  then
    echo "empty reading"
  else
    echo $TIMESTAMPNSEC,$RSSI1,$RSSI2,$RSSI3>>$1

    STRENGTH1=$(Get_Strength $RSSI1)
    STRENGTH2=$(Get_Strength $RSSI2)
    STRENGTH3=$(Get_Strength $RSSI3)

    Trigger_LED $STRENGTH1 $OLD_STRENGTH1 $LED1 1 $RSSI1
    Trigger_LED $STRENGTH2 $OLD_STRENGTH2 $LED2 2 $RSSI2
    Trigger_LED $STRENGTH3 $OLD_STRENGTH3 $LED3 3 $RSSI3


    OLD_STRENGTH1=$STRENGTH1
    OLD_STRENGTH2=$STRENGTH2
    OLD_STRENGTH3=$STRENGTH3
  fi
  # sleep 3  
done

exit

