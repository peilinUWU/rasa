## story new
* user.hello
  - action_greet
  - slot{"greeted": true}


## story - user first greet refuse give email
* user.hello
  - action_greet
* user.reject OR deny
  - utter_reply.to.reject
  - utter_greet.bye
  - action_deactivate_form
  - form{"name": null}




<!---------------------------->
<!-- generic conversations  -->
<!---------------------------->

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
  - utter_greet.bye

## story - affirm deny
* affirm OR deny
  - utter_acknowledge

## story - affirm v2
* affirm 
  - utter_great

## story - user ask question
* user.question
  - utter_reply.to_questions

## story - user ask how doing
* ask_howdoing
  - utter_reply.to_howdoing

## story - user insult
* user.insult
  - utter_reply.to_insult

## story - user nice to meet you
* nicetomeeyou
  - utter_reply.to_nicetomeetyou

## story - user enter data
* enter_data
  - utter_acknowledge

<!---------------------------->
<!--       chit chat        -->
<!---------------------------->

## chit chat - non english
* chit_chat_non_english
  - utter_default
    
## chit chat
* chit_chat
  - utter_default

## bot challenge
* bot_challenge
  - utter_iamabot

## user reject
* user.reject
  - utter_reply.to.reject
  - utter_greet.bye