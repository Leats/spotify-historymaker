import React from 'react';

class Overview extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
      error: null,
      isLoaded: false,
      items: [],
      artists: {},
      tracks: {}
      };
    }
    componentDidMount() {
      fetch("/data/played")
      .then(res => res.json())
      .then(
        (result) => {
        this.setState({
          isLoaded: true,
          items: result.items,
          artists: result.artists,
          tracks: result.tracks
        });
        },
        (error) => {
        this.setState({
          isLoaded: true,
          error
        });
        }
      )
    }
    render() {
      const { error, isLoaded, items } = this.state
      if (error) {
      return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
      return <div>Loading...</div>;
      } else {
          console.log(items)
      return (<div>Loaded :)</div>);
      }
    }
  }
  export default Overview;