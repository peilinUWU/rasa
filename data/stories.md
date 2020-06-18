## story
* user.hello
  - action_greet
  - slot{"greeted": true}
* affirm OR chit_chat_question OR chit_chat
  - action_add_on_1
* affirm OR chit_chat_question OR chit_chat
  - action_add_on_2

## story - user first greet refuse give email
* user.hello
  - action_greet
  - slot{"greeted": true}
* user.reject OR deny
  - utter_reply.to.reject
  - utter_greet.bye
  - action_deactivate_form
  - form{"name": null}


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

## Generated 1
* user.hello
  - action_greet
  - slot{"greeted":true}
  - request_email
  - form{"name":"request_email"}
  - slot{"requested_slot":"email"}
* enter_data
  - request_email
  - slot{"email":"sheep1@google.com"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - action_take_path
  - ask_name
  - form{"name":"ask_name"}
  - slot{"requested_slot":"name"}
* chit_chat_question{"PERSON":"Jack"}
  - ask_name
  - slot{"name":"Jack"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - request_fav_sport
  - form{"name":"request_fav_sport"}
  - slot{"requested_slot":"type_of_sport"}
* enter_data{"sport":"football"}
  - request_fav_sport
  - slot{"type_of_sport":"football"}
  - form{"name":null}
  - slot{"requested_slot":null}
* affirm OR chit_chat_question OR chit_chat
  - action_add_on_1