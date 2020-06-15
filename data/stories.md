## story 1
* user.hello
  - action_greet
  - slot{"greeted": true}
* enter_data{"PERSON": "Peter"}
  - action_topic_sport_1
* affirm OR chit_chat_question OR chit_chat
  - action_topic_sport_2
* affirm OR chit_chat_question OR chit_chat
  - action_topic_animal


## story - user first greet refuse give email
* user.hello
  - action_greet
  - slot{"greeted": true}
* user.reject OR deny
  - utter_reply.to.reject
  - utter_greet.bye
  - action_deactivate_form
  - form{"name": null}


## story - chit chat
* user.hello
  - action_greet
  - slot{"greeted": true}
* chit_chat_question OR chit_chat
  - action_get_answer
  - request_email



<!---------------------------->
<!-- default conversations  -->
<!---------------------------->

## story - default 1
* affirm
  - action_get_answer

## story - default 2
* user.thank
  - action_get_answer

## story - default 3
* user.sad
  - action_get_answer

## story - default 4
* user.good
  - action_get_answer

## story - default 5
* user.bye  
  - utter_greet.bye

## story - default 6
* user.insult
  - utter_reply.to_insult

## story - default 7
* nice_to_meet_you
  - utter_reply.to_nice_to_meet_you

## story - default 8
* enter_data
  - utter_acknowledge
  - action_self_disclosure

## story - default 9
* user.reject
  - utter_reply.to.reject
  - utter_greet.bye


<!---------------------------->
<!--       chit chat        -->
<!---------------------------->

## chit chat 1
* chit_chat_non_english
  - utter_only_english
    
## chit chat 2
* chit_chat
  - action_get_answer

## chit chat 3
* chit_chat_question
  - action_get_answer

## chit chat 4
* bot_challenge
  - action_get_answer
