const winston = require('winston');
const Transport = require('winston-transport');

// class MetricsTransport extends Transport {
//     constructor(opts) {
//         super(opts);
//         this.fileTransport = new winston.transports.File({
//             filename: 'remote-metrics.log',
//             level: 'info',
//             format: winston.format.combine(
//                 winston.format.timestamp(),
//                 winston.format.prettyPrint() // << pretty JSON format
//             )
//         });
//     }

//     log(info, callback) {
//         if (info.message && typeof info.message === 'object' && info.message.type === 'metrics') {
//             this.fileTransport.log(info, callback);
//         } else {
//             callback();
//         }
//     }
// }

class MetricsTransport extends Transport {
    constructor(opts) {
        super(opts);
        this.fileTransport = new winston.transports.File({
            filename: 'remote-metrics.log',
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.prettyPrint()
            )
        });
    }

    log(info, callback) {
        if (info.message && typeof info.message === 'object' && info.message.type === 'metrics') {
            this.fileTransport.log(info, callback);

            // ✅ Also log to console for visibility in CI/CD
            const label = info.message.label || '';
            const output = info.message.output || '';
            const host = info.message.host || '';
            console.log(`[REMOTE METRICS] ${label} ${host} :: ${output}`);
        }
        callback();
    }
}


const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'jmeter_execution.log' }),
        new MetricsTransport()
    ]
});

module.exports = logger;
