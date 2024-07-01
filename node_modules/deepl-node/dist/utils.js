"use strict";
// Copyright 2022 DeepL SE (https://www.deepl.com)
// Use of this source code is governed by an MIT
// license that can be found in the LICENSE file.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.toBoolString = exports.isString = exports.timeout = exports.streamToString = exports.streamToBuffer = exports.logInfo = exports.logDebug = void 0;
const loglevel_1 = __importDefault(require("loglevel"));
const logger = loglevel_1.default.getLogger('deepl');
function concatLoggingArgs(args) {
    let detail = '';
    if (args) {
        for (const [key, value] of Object.entries(args)) {
            detail += `, ${key} = ${value}`;
        }
    }
    return detail;
}
function logDebug(message, args) {
    logger.debug(message + concatLoggingArgs(args));
}
exports.logDebug = logDebug;
function logInfo(message, args) {
    logger.info(message + concatLoggingArgs(args));
}
exports.logInfo = logInfo;
/**
 * Converts contents of given stream to a Buffer.
 * @private
 */
async function streamToBuffer(stream) {
    const chunks = [];
    return new Promise((resolve, reject) => {
        stream.on('data', (chunk) => chunks.push(chunk));
        stream.on('error', (err) => reject(err));
        stream.on('end', () => resolve(Buffer.concat(chunks)));
    });
}
exports.streamToBuffer = streamToBuffer;
/**
 * Converts contents of given stream to a string using UTF-8 encoding.
 * @private
 */
async function streamToString(stream) {
    return (await streamToBuffer(stream)).toString('utf8');
}
exports.streamToString = streamToString;
// Wrap setTimeout() with Promise
const timeout = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
exports.timeout = timeout;
/**
 * Returns true if the given argument is a string.
 * @param arg Argument to check.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function isString(arg) {
    return typeof arg === 'string';
}
exports.isString = isString;
/**
 * Returns '1' if the given arg is truthy, '0' otherwise.
 * @param arg Argument to check.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function toBoolString(arg) {
    return arg ? '1' : '0';
}
exports.toBoolString = toBoolString;
