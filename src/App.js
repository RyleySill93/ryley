import React from 'react';
import './App.css';
import axios from 'axios';


class App extends React.Component {
    componentDidMount() {
        axios.get('http://localhost:8000/accounts/').then(res => {
            debugger
            this.setState({ accounts: res.data });
        })
    }

    render() {
        return (
            <div className="App">
                <table>
                    <tr>
                        <th>
                            Account
                        </th>
                        <th>
                            Credit
                        </th>
                        <th>
                            Debit
                        </th>
                    </tr>
                    {
                        [1,1,1,1,1,1,1,1,1].map(_ => (
                            <tr>
                                <td><input type="button" value="choose account" /></td>
                                <td><input /></td>
                                <td><input /></td>
                            </tr>
                        ))
                    }
                </table>
                <div>

                </div>
            </div>
        );
    }
}

export default App;
