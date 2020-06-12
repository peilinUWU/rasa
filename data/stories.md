## story new
* user.hello
  - action_greet
  - slot{"greeted": true}


## story - user first greet refuse give email
* user.hello
  - action_greet
  - slot{"greeted": true}
* user.reject OR deny
  - utter_reply.to.reject
  - utter_greet.bye
  - action_deactivate_form
  - form{"name": null}


## story - 
* user.hello
  - action_greet
  - slot{"greeted": true}
* chit_chat_question OR chit_chat
  - action_get_answer
  - request_email


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

## story - user insult
* user.insult
  - utter_reply.to_insult

## story - user nice to meet you
* nice_to_meet_you
  - utter_reply.to_nice_to_meet_you

## story - user enter data
* enter_data
  - utter_acknowledge
  - action_self_disclosure

<!---------------------------->
<!--       chit chat        -->
<!---------------------------->


## chit chat - non english
* chit_chat_non_english
  - utter_only_english
    
## chit chat
* chit_chat
  - action_get_answer

## story - user ask question
* chit_chat_question
  - action_get_answer

## bot challenge
* bot_challenge
  - action_get_answer

## user reject
* user.reject
  - utter_reply.to.reject
  - utter_greet.bye