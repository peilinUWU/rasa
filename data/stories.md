

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
  - action_set_reminder

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

## Generated 1
* user.hello
  - action_greet
  - slot{"greeted":true}
  - request_email
  - form{"name":"request_email"}
  - slot{"requested_slot":"email"}
* enter_data
  - request_email
  - slot{"email":"test12@google.com"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - action_take_path
  - ask_name
  - form{"name":"ask_name"}
  - slot{"requested_slot":"name"}
* chit_chat
  - ask_name
  - slot{"name":"my name is haldan"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - action_topic_sport_1
  - request_sport_detail_1
  - form{"name":"request_sport_detail_1"}
  - slot{"requested_slot":"type_of_sport"}
* enter_data{"sport":"football"}
  - request_sport_detail_1
  - slot{"type_of_sport":"football"}
  - form{"name":null}
  - slot{"requested_slot":null}
* affirm
  - action_topic_sport_2