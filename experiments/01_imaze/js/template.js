var condition = parseInt(window.location.search.replace("?cond=", ""))


var trial_counter = 0;

function build_trials() {

  var stim_list = stims[condition];
  for (var i = 0; i < fillers.length; i++) {
    stim_list.push(fillers[i]);
  }

  stim_list = _.shuffle(stim_list)
  stim_list.splice(0,0, practice_items[0], practice_items[1], practice_items[2])
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

      $(".error").hide();
      $("#maze-wrapper").show();
      $("#intermission").hide();


      this.stim = stim;
      this.position = 0;

      this.response_times = [];

      this.words = [];
      this.words[0] = stim.s1.split(" ");
      this.words[1] = stim.s2.split(" ");

      this.max_length = Math.max(this.words[0].length, this.words[1].length);
      this.min_length = Math.min(this.words[0].length, this.words[1].length);

      this.critical_position = -1;
      for (var i = 0; i < this.min_length; i++) {
        if (this.words[0][i] != this.words[1][i]) {
          this.critical_position = i;
          break;
        }
      }

      //TODO: adapt for multi-path maze
      this.awords = [];
      this.awords[0] = stim.a1.split(" ");
      this.awords[1] = stim.a2.split(" ");

      this.path = 0;


      this.order = [];
      for (var i = 0; i < this.max_length; i++) {
        this.order.push(_.random(1));
      }

      var lword = this.order[this.position] == 0 ? this.words[this.path][this.position] : this.awords[this.path][this.position];
      var rword = this.order[this.position] == 0 ? this.awords[this.path][this.position] : this.words[this.path][this.position];

      $("#lword").text(lword);
      $("#rword").text(rword);

      var t = this;

      t.correct = [];

      this.response_times.push(Date.now());
      $(document).bind("keydown", function(evt) {
        if (evt.keyCode == 69 || evt.keyCode == 73) {
          evt.preventDefault();
          var pressed_e = evt.keyCode == 69;
          var pressed_i = evt.keyCode == 73;

          var correct = false;
          if (t.position == t.critical_position ||
              (pressed_e && t.order[t.position] == 0) ||
              (pressed_i && t.order[t.position] == 1)
            ) {
              correct = true;
            }

          if (t.correct.length == (t.response_times.length - 1)) {
            t.correct.push(correct);
          }


          if (!correct) {
            $(".error").show();
          } else {
            $(".error").hide();
            t.response_times.push(Date.now());
            if (t.position == t.critical_position) {
              if ((pressed_i &&  t.order[t.position] == 0) ||
                  (pressed_e && t.order[t.position] == 1)
                ) {
                  t.path = 1;
                }
            }

            t.position++;

            if (t.position < t.words[t.path].length) {
              if (t.position != t.critical_position) {
                var lword = t.order[t.position] == 0 ? t.words[t.path][t.position] : t.awords[t.path][t.position];
                var rword = t.order[t.position] == 0 ? t.awords[t.path][t.position] : t.words[t.path][t.position];
              } else {
                var lword = t.order[t.position] == 0 ? t.words[0][t.position] : t.words[1][t.position];
                var rword = t.order[t.position] == 0 ? t.words[1][t.position] : t.words[0][t.position];
              }
              $("#lword").text(lword);
              $("#rword").text(rword);
            } else {
              $(document).unbind("keydown");
              t.log_responses();
              $("#intermission").show();
              $("#maze-wrapper").hide();
              $(document).bind("keydown", function(evt) {
                evt.preventDefault();
                $(document).unbind("keydown");
                _stream.apply(t);
              });
            }
          }
        }
      });
    },

    log_responses : function() {
      for (var i = 0; i < this.words[this.path].length; i++) {
        var word = this.words[this.path][i];
        exp.data_trials.push({
          "trial_id": this.stim.trial_id,
          "word_idx": i,
          "rt": this.response_times[i+1] - this.response_times[i],
          "correct": this.correct[i] ? 1 : 0,
          "trial_no": trial_counter,
          "path": this.path,
          "word": word,
          "alternative": this.awords[this.path][i],
          "order": this.order[i]
        });
      }
      trial_counter++;
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
