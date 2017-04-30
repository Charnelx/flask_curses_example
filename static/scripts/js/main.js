(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var DynamicSearch = React.createClass({displayName: "DynamicSearch",

  // sets initial state
  getInitialState: function(){
    return { searchString: '' , data: {"result": []}};
  },

  // sets state, triggers render method
  handleChange: function(event){
    // grab value form input box
    this.setState({searchString:event.target.value});
  },

  async loadArticles() {
       var csrftoken = $('meta[name=csrf-token]').attr('content');
       // console.log(csrftoken);

       this.setState({
           data: await fetch("/", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': csrftoken
                    },
                    credentials: 'include',
                    body: JSON.stringify({})
        }).then(response =>response.json())
       })
   },

   componentDidMount() {
       this.loadArticles();
   },

  render: function() {

    var topics = this.state.data.result;
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter topics list by value from input box
    if(searchString.length > 0){
      topics = topics.filter(function(topic){
        return topic.title.toLowerCase().match( searchString ) || topic.author.toLowerCase().match( searchString );
      });
    }
    return (
      React.createElement("div", null, 
        React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, placeholder: "Search!"}), 
        React.createElement("ul", {className: "messages"}, 
            topics.map(function(topic) {
                return React.createElement("li", null,  topic.author, React.createElement("p", null, React.createElement("strong", null,  topic.title)), React.createElement("p", null, React.createElement("a", {href: topic.url}, "Link")))
            })
        )
      )
    )
  }

});

ReactDOM.render(
  React.createElement(DynamicSearch, null),
  document.getElementById('main')
);

},{}]},{},[1]);
