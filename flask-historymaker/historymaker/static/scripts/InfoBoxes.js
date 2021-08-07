import React from 'react';

class InfoBoxes extends React.Component {
    render() {
        return (
            <div>
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">Overview</h1>
                    <div class="btn-toolbar mb-2 mb-md-0">
                        <button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
                            <span data-feather="calendar"></span>
                This week
                </button>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">Favorite Song</h5>
                                <p class="card-text">Title by Artist</p>
                                <a href="#" class="card-link">View on Spotify</a>
                                <a href="#" class="card-link">Another link</a>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">Favorite Artist</h5>
                                <p class="card-text">Artist Name</p>
                                <a href="#" class="card-link">View on Spotify</a>
                                <a href="#" class="card-link">Another link</a>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">Favorite Genre</h5>
                                <p class="card-text">Artist Name</p>
                                <a href="#" class="card-link">View on Spotify</a>
                                <a href="#" class="card-link">Another link</a>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">Time Listened</h5>
                                <p class="card-text">10000 Min</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
export default InfoBoxes;