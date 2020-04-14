
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
  - form{"name": null}
  - action_ask_reason


## story - reply to reason 1
* inform_reason{"reason":"cool"}
  - utter_thumbsup

## story - reply to reason 2
* inform_reason{"reason":"cool"}
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