# ホタル誘引Ｌチカ　静御前  V1.0
# Author: Shigeaki Tendo
# 2023.06.02 First release.

from machine import Pin, PWM
import math
import utime


def get_pulse_count(firefly_type):	# １回の発光あたりのパルス出力数を計算
    return(firefly_type * 5000.0)


Heike = 1.2				# ヘイケボタルの発光周期（秒）
Genji = 2.0				# ゲンジボタルの発光周期（秒）
Duty_100 = 65535			# 最大発光時のデューティレンジ

firefly = Heike				# 初期起動時はヘイケボタルモード
pulse_count = get_pulse_count(firefly)

ModeSw = Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)		# モードスイッチ(Heike/Genji切り替え) GPIO#16
led = Pin("LED", Pin.OUT)					# 内部LED初期化
yellow = PWM(Pin(14))						# 出力用外部LED端子 GPIO#14
yellow.freq(100_000)						# PWM周波数 100KHz

while True:
    if ModeSw.value() == 1:
        led.on()						# モードスイッチを押下中、内蔵LEDを点灯
        while ModeSw.value() == 1:
            pass
        if firefly == Heike:
            firefly = Genji
        else:
            firefly = Heike
        pulse_count = get_pulse_count(firefly)
        led.off()
    for i in range(pulse_count):
        yellow.duty_u16(int(Duty_100*math.exp(-(float(i*2)/(pulse_count/2.0)-2.0)**2.0)))	#duty u16/65535
        utime.sleep_us(1)
    yellow.duty_u16(0)
    utime.sleep(firefly/2.0)
