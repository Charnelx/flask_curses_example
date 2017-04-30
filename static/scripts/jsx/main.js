var DynamicSearch = React.createClass({

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
       this.setState({
           data: await fetch("/", {
                    credentials: 'include',
                    method: "POST",
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
      <div>
        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
        <ul className="messages">
            {topics.map(function(topic) {
                return <li>{ topic.author }<p><strong>{ topic.title }</strong></p><p><a href={topic.url}>Link</a></p></li>
            })}
        </ul>
      </div>
    )
  }

});

ReactDOM.render(
  <DynamicSearch />,
  document.getElementById('main')
);