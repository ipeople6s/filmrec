import {assign, map} from "lodash";
import {request} from "./service";

const files = require.context("./modules", true, /\.js$/);
const generators = files.keys().map(key => ({
    name: key.replace(/\.js$/g, '').replace(/\.\//g, ''),
    api: files(key).default
}));

export default assign(
    {},
    ...map(generators, generator => ({
            [generator.name]: generator.api({
                request
            })
        })
    )
);