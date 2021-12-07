var condition = parseInt(window.location.search.replace("?cond=", ""))


var trial_counter = 0;

function build_trials() {

  var stim_list = stims[condition];
  for (var i = 0; i < fillers.length; i++) {
    stim_list.push(fillers[i]);
  }

  stim_list = _.shuffle(stim_list)
  stim_list.splice(0,0, practice_items[0], practice_items[1])
  return stim_list;
}



function make_slides(f) {
  var   slides = {};

  slides.i0 = slide({
     name : "i0",
     start: function() {
      exp.startT = Date.now();
     }
  });

  slides.instructions = slide({
    name : "instructions",
    button : function() {
      exp.go(); //use exp.go() if and only if there is no "present" data.
    }
  });


  slides.trial = slide({
    name: "trial",
    present: exp.train_stims,
    present_handle: function(stim) {

      this.stim = stim;
      $("#prompt-wrapper").text(stim.prompt);
    
      stim.order = _.random(1);
      if (stim.order == 1) {
        $("#continuation-1").text(stim.unexp_continuation);
        $("#continuation-2").text(stim.exp_continuation);
        $("#continuation-1").data("val", "unexp");
        $("#continuation-2").data("val", "exp");
        
      } else {
        $("#continuation-1").text(stim.exp_continuation);
        $("#continuation-2").text(stim.unexp_continuation);
        $("#continuation-1").data("val", "exp");
        $("#continuation-2").data("val", "unexp");
        
      }
      
      $("#continuation-1, #continuation-2").unbind("click");
      
      var t = this;
      $("#continuation-1, #continuation-2").click(function() {
        t.log_responses($(this).data("val"));
      });
      

     
    },

    log_responses : function(response) {
      
      exp.data_trials.push({
        "id": this.stim.id,
        "prompt": this.stim.prompt,
        "exp_continuation": this.stim.exp_continuation,
        "unexp_continuation": this.stim.unexp_continuation,
        "response": response,
        "type": this.stim.type || "filler",
        "order": this.stim.order
      });
      _stream.apply(this);
    }
  });




  slides.subj_info =  slide({
    name : "subj_info",
    submit : function(e){
      //if (e.preventDefault) e.preventDefault(); // I don't know what this means.
      exp.subj_data = {
        language : $("#language").val(),
        other_language: $("#other-language").val(),
        enjoyment: $("#enjoyment").val(),
        problems: $("#problems").val(),
        asses: $('input[name="assess"]:checked').val(),

        age: $("#age").val(),
        gender: $("#gender").val(),
        education: $("#education").val(),
        fairprice: $("#fairprice").val(),
        comments: $("#comments").val()
      };
      exp.go(); //use exp.go() if and only if there is no "present" data.
    }
  });

  slides.thanks = slide({
    name : "thanks",
    start : function() {
      exp.data= {
          "trials" : exp.data_trials,
          "catch_trials" : exp.catch_trials,
          "system" : exp.system,
          "condition" : exp.condition,
          "subject_information" : exp.subj_data,
          "time_in_minutes" : (Date.now() - exp.startT)/60000
      };
      proliferate.submit(exp.data);
    }
  });

  return slides;
}

/// init ///
function init() {
  exp.condition = condition;
  exp.trials = [];
  exp.catch_trials = [];
  exp.train_stims = build_trials(); //can randomize between subject conditions here
  exp.system = {
      Browser : BrowserDetect.browser,
      OS : BrowserDetect.OS,
      screenH: screen.height,
      screenUH: exp.height,
      screenW: screen.width,
      screenUW: exp.width
    };
  //blocks of the experiment:
  exp.structure=["i0",  "instructions", "trial", 'subj_info', 'thanks'];

  exp.data_trials = [];
  //make corresponding slides:
  exp.slides = make_slides(exp);

  exp.nQs = utils.get_exp_length(); //this does not work if there are stacks of stims (but does work for an experiment with this structure)
                    //relies on structure and slides being defined

  $('.slide').hide(); //hide everything

  //make sure turkers have accepted HIT (or you're not in mturk)
  $("#start_button").click(function() {
      exp.go();
  });

  $(".response-buttons, .test-response-buttons").click(function() {
    _s.button($(this).val());
  });

  exp.go(); //show first slide
}
