<!DOCTYPE html>
<html>
<head>
    <title>Scruffy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=no">
    <script type="text/javascript" src="/static/zepto.min.js"></script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <style>
    body {
        padding: 0;
        margin: 0;
    }
    form {
        float: left;
        vertical-align: top;
        width: 62%;
        transition: 400ms;
    }
    .hide form {
        opacity: 0;
    }
    textarea {
        background: #ffe;
        width: 100%;
        height: 220px;
    }
    img {
        width: 100%;
        vertical-align: top;
    }
    h2 {
        text-transform: capitalize;
    }
    input.clipboard {
        width: 500px;
    }
    .on-hover {
        position: absolute;
        top: 0;
        left: 0;
        vertical-align: top;
        transition: 400ms;
    }
    .show .on-hover {
        left: 62%;
        margin-left: 10px;
    }
    .show-on-hover {
        opacity: 0;
        visibility: hidden;
        transition: 0.6s ease-in-out;
        color: #999;
        font-size: smaller;
    }
    .show .show-on-hover,
    .on-hover:hover .show-on-hover {
        opacity: 1;
        visibility: initial;
    }

    @media (min-width: 700px) {
        body {
            margin: 10px;
        }
    }

    @media (min-height: 550px) {
        .show .on-hover {
            top: 300px;
            left: 0;
        }
        form {
            width: 100%;
        }
        img {
            max-width: 100%;
            margin-left: 0;
        }
    }
    </style>
</head>
<body class="show">
    <form action="/{{type}}/" method="GET">
        <textarea name="spec" autofocus="autofocus">{{spec}}</textarea>
        <div>
          See <a href="https://github.com/aivarsk/scruffy/blob/master/README.rst#{{type}}-diagrams" target="_blank">Scruffy syntax</a>.
          New <a href="/class/">class diagram</a>, <a href="/sequence/">sequence diagram</a>.
        </div>
        <input type="submit"/>
    </form>
    <div class="on-hover">
        <a href="#" title="Click to toggle edit mode"><img src="{{type}}/{{encoded_spec}}.png" /></a>
        <div class="show-on-hover">
            Also available as <a id="svg-export" href="/{{type}}/{{encoded_spec}}.svg" title="SVG Vector Graphics" target="_blank">SVG</a> and <a id="pdf-export" href="/{{type}}/{{encoded_spec}}.pdf" title="PDF Document" target="_blank">PDF</a>
        </div>
    </div>
    <script type="text/javascript">
var umlTextarea = $('textarea');
var umlImage = $('img');

// Update when the input text is changed (after a short delay).
(function() {
  var update = function() {
    var spec = umlTextarea.val().replace(/(\r\n|\n|\r)/gm, ',');
    if (!spec) {
      spec = ' ';
    }
    var specUri = encodeURIComponent(spec);
    umlImage.attr('src', specUri + '.png');

    // Change the current URL after unencoding some pretty safe characters.
    specUri = specUri.replace('%3C', '<').replace('%3E', '>');
    specUri = specUri.replace('%7B', '{').replace('%7D', '}');
    specUri = specUri.replace('%26', '&');
    specUri = specUri.replace('%2B', '+');
    specUri = specUri.replace('%2C', ',');
    specUri = specUri.replace('%3A', ':');
    specUri = specUri.replace('%3B', ';');
    specUri = specUri.replace('%3D', '=');
    specUri = specUri.replace('%24', '$');
    specUri = specUri.replace('%40', '@');
    specUri = specUri.replace('%7C', '|');

    window.history.pushState('Scruffy', 'Scruffy', '/{{type}}/' + specUri);
    $('#svg-export').attr('href', '/{{type}}/' + specUri + '.svg');
    $('#pdf-export').attr('href', '/{{type}}/' + specUri + '.pdf');
  };
  var delay = (function() {
    var timer = 0;
    return function(callback, ms) {
      clearTimeout (timer);
      timer = setTimeout(callback, ms);
    };
  })();
  umlTextarea.on('input', function() {
    delay(update, 300);
  });
})();

// Show/hide the input textarea.
(function() {
  var inputForm = $('form');

  var show = function() {
    $('body').removeClass('hide');
    $('body').addClass('show');
    umlTextarea.focus();
    return false;
  };

  var hide = function() {
    // If the UML was successfully generated, hide the image.
    if (umlImage.width() + umlImage.height() > 50) {
      $('body').addClass('hide');
      $('body').removeClass('show');
    }
  };

  // Toggle display input on click image.
  var visible = true;
  umlImage.click(function() {
    if ($('body').hasClass('show')) {
      hide();
    } else {
      show();
    }
    return false;
  });

  // Display input on key press.
  $('html').keypress(function(e) {
    show();
  });

  // Hide on key ESC, show on arrow keys.
  $('html').keydown(function(e) {
    if (e.keyCode == 27) {
      hide();
    } else if (e.keyCode >= 37 && e.keyCode <= 40) {
      show();
    }
  });

  // Hide input when clicking outside.
  $('html').click(function() {
    hide();
  });
  umlTextarea.click(function() {
    return false;
  });

  // Select all on inputs.
  $('input.clipboard').click(function() {
    $(this).select();
  })

  % if autocollapse:
  setTimeout(hide, 1000);
  % end
})();

// Hide the "Submit" button.
$('input[type=submit]').hide();
    </script>
</body>
</html>
