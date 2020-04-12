## story 001
* topic
  - action_get_topic
  - answer_form
  - form{"name": "answer_form"}
  - slot{"requested_slot": "type_of_sport"}
* form: inform{"sport": "football"}
  - action_get_detail
  - form: answer_form
  - slot{"type_of_sport": "football"}
  - slot{"requested_slot": "reason_sport"}
* form: inform_reason{"reason":"cool"}
  - form: answer_form
  - slot{"reason_sport": "cool"}
  - form{"name": null}
  - utter_great

## story 002
* topic
  - action_get_topic
  - answer_form
  - form{"name": "answer_form"}
  - slot{"requested_slot": "type_of_animal"}
* form: inform{"animal": "cat"}
  - form: answer_form
  - slot{"type_of_animal": "cat"}
  - slot{"requested_slot": "reason_animal"}
* form: inform_reason{"reason":"cute"}
  - form: answer_form
  - slot{"reason_animal": "cute"}
  - form{"name": null}
  - utter_great

## story 01
* user.hello
  - utter_greet.hi
  - utter_ask_topic
* sport
  - action_get_topic
  - answer_form
  - form{"name": "answer_form"}
  - slot{"requested_slot": "type_of_sport"}
* form: inform{"sport": "football"}
  - action_get_detail
  - form: answer_form
  - slot{"type_of_sport": "football"}
  - slot{"requested_slot": "reason_sport"}
* form: inform_reason{"reason":"cool"}
  - form: answer_form
  - slot{"reason_sport": "cool"}
  - form{"name": null}
  - utter_great

## story 02
* user.hello
  - utter_greet.hi
  - utter_ask_topic
* animal
  - action_get_topic
  - answer_form
  - form{"name": "answer_form"}
  - slot{"requested_slot": "type_of_animal"}
* form: inform{"animal": "dog"}
  - action_get_detail
  - form: answer_form
  - slot{"type_of_animal": "dog"}
  - slot{"requested_slot": "reason_animal"}
* form: inform_reason{"reason":"fun"}
  - form: answer_form
  - slot{"reason_animal": "fun"}
  - form{"name": null}
  - utter_great
  

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
  - utter_temp

## story - affirm deny
* affirm OR deny
  - utter_thumbsup

## story - affirm v2
* affirm 
  - utter_great
  

<!---------------------------->
<!--     out of scope       -->
<!---------------------------->


## out of scope - non english
* out.of.scope.non.english
  - utter_reply.to_out_of_scope_non_english
    
## out of scope - other
* out.of.scope.other
  - utter_reply.to_out_of_scope_other

## bot challenge
* bot_challenge
  - utter_iamabot