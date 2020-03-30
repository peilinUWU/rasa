## story sport
* sport {"topic" : "sport"}
  - utter_sport

## story animal 
* animal {"topic" : "animal"}
  - utter_animal

## story food 
* food {"topic" : "food"}
  - utter_food

## story travel 
* travel {"topic" : "travel"}
  - utter_travel
    
    
<!---------------------------->
<!-- generic conversations  -->
<!---------------------------->

## story 01
* user.hello
  - utter_greet.hi
  - utter_greet.ask_topic
* sport OR animal OR food OR travel
  - action_choose_topic
  - slot{"topic" : "food"}

## story - thank
* user.thank
  - utter_reply.to_thank

## story - sad
* user.sad
  - utter_reply.to_sad

## story - good
* user.good
  - utter_reply.to_good

## story - bye
* user.bye  
  - utter_temp

## story - affirm / deny
* affirm OR deny
  - utter_thumbsup

## story - affirm v2
* affirm 
  - utter_great
  
<!---------------------------->
<!--     out of scope       -->
<!---------------------------->

## out of scope non english
* out_of_scope/non_english
  - I only understand English, I'm sorry.

## out of scope other
* out_of_scope/other
  - I can't help you with that, I'm sorry.
