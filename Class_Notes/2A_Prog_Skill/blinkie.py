from blinkstick import blinkstick

#find the blinkstick 
bs = blinkstick.find_first()  #is it connected? 
if bs is None:
    print('Please connect the blinkstick.') 

else:     # now set both info blocks to the text Not Set.     
    bs.set_info_block1('Not Set')
    bs.set_info_block2('Not Set')
    print('Info blocks cleared.')