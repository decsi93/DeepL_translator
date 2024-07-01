"use strict";
// Copyright 2022 DeepL SE (https://www.deepl.com)
// Use of this source code is governed by an MIT
// license that can be found in the LICENSE file.
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseDocumentHandle = exports.parseGlossaryLanguagePairArray = exports.parseLanguageArray = exports.parseTextResultArray = exports.parseUsage = exports.parseDocumentStatus = exports.parseGlossaryInfoList = exports.parseGlossaryInfo = void 0;
const errors_1 = require("./errors");
const index_1 = require("./index");
class UsageDetailImpl {
    /**
     * @private Package users should not need to construct this class.
     */
    constructor(count, limit) {
        this.count = count;
        this.limit = limit;
    }
    limitReached() {
        return this.count >= this.limit;
    }
}
class UsageImpl {
    /**
     * @private Package users should not need to construct this class.
     */
    constructor(character, document, teamDocument) {
        this.character = character;
        this.document = document;
        this.teamDocument = teamDocument;
    }
    /** Returns true if any usage type limit has been reached or passed, otherwise false. */
    anyLimitReached() {
        var _a, _b, _c;
        return (((_a = this.character) === null || _a === void 0 ? void 0 : _a.limitReached()) ||
            ((_b = this.document) === null || _b === void 0 ? void 0 : _b.limitReached()) ||
            ((_c = this.teamDocument) === null || _c === void 0 ? void 0 : _c.limitReached()) ||
            false);
    }
    /** Converts the usage details to a human-readable string. */
    toString() {
        const labelledDetails = [
            ['Characters', this.character],
            ['Documents', this.document],
            ['Team documents', this.teamDocument],
        ];
        const detailsString = labelledDetails
            .filter(([, detail]) => detail)
            .map(([label, detail]) => `${label}: ${detail.count} of ${detail.limit}`);
        return 'Usage this billing period:\n' + detailsString.join('\n');
    }
}
class DocumentStatusImpl {
    constructor(status, secondsRemaining, billedCharacters, errorMessage) {
        this.status = status;
        this.secondsRemaining = secondsRemaining;
        this.billedCharacters = billedCharacters;
        this.errorMessage = errorMessage;
    }
    ok() {
        return this.status === 'queued' || this.status === 'translating' || this.status === 'done';
    }
    done() {
        return this.status === 'done';
    }
}
/**
 * Parses the given glossary info API response to a GlossaryInfo object.
 * @private
 */
function parseRawGlossaryInfo(obj) {
    return {
        glossaryId: obj.glossary_id,
        name: obj.name,
        ready: obj.ready,
        sourceLang: obj.source_lang,
        targetLang: obj.target_lang,
        creationTime: new Date(obj.creation_time),
        entryCount: obj.entry_count,
    };
}
/**
 * Parses the given JSON string to a GlossaryInfo object.
 * @private
 */
function parseGlossaryInfo(json) {
    try {
        const obj = JSON.parse(json);
        return parseRawGlossaryInfo(obj);
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
exports.parseGlossaryInfo = parseGlossaryInfo;
/**
 * Parses the given JSON string to an array of GlossaryInfo objects.
 * @private
 */
function parseGlossaryInfoList(json) {
    try {
        const obj = JSON.parse(json);
        return obj.glossaries.map((rawGlossaryInfo) => parseRawGlossaryInfo(rawGlossaryInfo));
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
exports.parseGlossaryInfoList = parseGlossaryInfoList;
/**
 * Parses the given JSON string to a DocumentStatus object.
 * @private
 */
function parseDocumentStatus(json) {
    try {
        const obj = JSON.parse(json);
        return new DocumentStatusImpl(obj.status, obj.seconds_remaining, obj.billed_characters, obj.error_message);
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
exports.parseDocumentStatus = parseDocumentStatus;
/**
 * Parses the given usage API response to a UsageDetail object, which forms part of a Usage object.
 * @private
 */
function parseUsageDetail(obj, prefix) {
    const count = obj[`${prefix}_count`];
    const limit = obj[`${prefix}_limit`];
    if (count === undefined || limit === undefined)
        return undefined;
    return new UsageDetailImpl(count, limit);
}
/**
 * Parses the given JSON string to a Usage object.
 * @private
 */
function parseUsage(json) {
    try {
        const obj = JSON.parse(json);
        return new UsageImpl(parseUsageDetail(obj, 'character'), parseUsageDetail(obj, 'document'), parseUsageDetail(obj, 'team_document'));
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
exports.parseUsage = parseUsage;
/**
 * Parses the given JSON string to an array of TextResult objects.
 * @private
 */
function parseTextResultArray(json) {
    try {
        const obj = JSON.parse(json);
        return obj.translations.map((translation) => {
            return {
                text: translation.text,
                detectedSourceLang: (0, index_1.standardizeLanguageCode)(translation.detected_source_language),
            };
        });
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
exports.parseTextResultArray = parseTextResultArray;
/**
 * Parses the given language API response to a Language object.
 * @private
 */
function parseLanguage(lang) {
    try {
        const result = {
            name: lang.name,
            code: (0, index_1.standardizeLanguageCode)(lang.language),
            supportsFormality: lang.supports_formality,
        };
        if (result.supportsFormality === undefined) {
            delete result.supportsFormality;
        }
        return result;
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
/**
 * Parses the given JSON string to an array of Language objects.
 * @private
 */
function parseLanguageArray(json) {
    const obj = JSON.parse(json);
    return obj.map((lang) => parseLanguage(lang));
}
exports.parseLanguageArray = parseLanguageArray;
/**
 * Parses the given glossary language pair API response to a GlossaryLanguagePair object.
 * @private
 */
function parseGlossaryLanguagePair(obj) {
    try {
        return {
            sourceLang: obj.source_lang,
            targetLang: obj.target_lang,
        };
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
/**
 * Parses the given JSON string to an array of GlossaryLanguagePair objects.
 * @private
 */
function parseGlossaryLanguagePairArray(json) {
    const obj = JSON.parse(json);
    return obj.supported_languages.map((langPair) => parseGlossaryLanguagePair(langPair));
}
exports.parseGlossaryLanguagePairArray = parseGlossaryLanguagePairArray;
/**
 * Parses the given JSON string to a DocumentHandle object.
 * @private
 */
function parseDocumentHandle(json) {
    try {
        const obj = JSON.parse(json);
        return { documentId: obj.document_id, documentKey: obj.document_key };
    }
    catch (error) {
        throw new errors_1.DeepLError(`Error parsing response JSON: ${error}`);
    }
}
exports.parseDocumentHandle = parseDocumentHandle;
