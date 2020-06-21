## story - user first greet refuse give email
* user.hello
  - action_greet
* enter_data
  - action_set_name

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


<!---------------------------->
<!--      generated         -->
<!---------------------------->

## generated 1
* user.hello
  - action_greet
  - slot{"greeted":true}
  - request_email
  - form{"name":"request_email"}
  - slot{"requested_slot":"email"}
* enter_data
  - request_email
  - slot{"email":"sheep9@google.com"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - action_take_path
* chit_chat
  - action_set_name