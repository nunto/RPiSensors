import React, { Component } from 'react';
import { Feed, Icon } from 'semantic-ui-react';
import "./style/Home.css";


class HomePage extends Component {
    render () {
        return (
            <div class="feed-content">
                <Feed>
                    <Feed.Event>
                        <Feed.Label>
                            <Icon name='x' />
                        </Feed.Label>
                        <Feed.Content>
                            <Feed.Date>2018/20/7 10:05</Feed.Date>
                            <Feed.Summary>
                                RPM on device <a>Pi-2</a> dropped to 0.
                            </Feed.Summary>
                        </Feed.Content>
                    </Feed.Event>

                    <Feed.Event>
                        <Feed.Label>
                            <Icon name='x' />
                        </Feed.Label>
                        <Feed.Content>
                            <Feed.Date>2018/20/7 13:21</Feed.Date>
                            <Feed.Summary>
                                No current detected on device <a>Pi-4</a>.
                            </Feed.Summary>
                        </Feed.Content>
                    </Feed.Event>
                    
                    <Feed.Event>
                        <Feed.Label>
                            <Icon name='cloud upload' />
                        </Feed.Label>
                        <Feed.Content>
                            <Feed.Date>2018/20/7 16:48</Feed.Date>
                            <Feed.Summary>
                                <a title="View device">Pi-2</a> data successfully synced.
                            </Feed.Summary>
                        </Feed.Content>
                    </Feed.Event>

                </Feed>
            </div>
        )
    }
}

export default HomePage;
