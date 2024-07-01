/// <reference types="node" />
/// <reference types="node" />
export declare function logDebug(message: string, args?: object): void;
export declare function logInfo(message: string, args?: object): void;
/**
 * Converts contents of given stream to a Buffer.
 * @private
 */
export declare function streamToBuffer(stream: NodeJS.ReadableStream): Promise<Buffer>;
/**
 * Converts contents of given stream to a string using UTF-8 encoding.
 * @private
 */
export declare function streamToString(stream: NodeJS.ReadableStream): Promise<string>;
export declare const timeout: (ms: number) => Promise<unknown>;
/**
 * Returns true if the given argument is a string.
 * @param arg Argument to check.
 */
export declare function isString(arg: any): arg is string;
/**
 * Returns '1' if the given arg is truthy, '0' otherwise.
 * @param arg Argument to check.
 */
export declare function toBoolString(arg: any): string;
