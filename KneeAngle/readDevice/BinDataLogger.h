#ifndef BinDataLogger_h
#define BinDataLogger_h

struct block_t {
  unsigned short count;    // count of data values
  unsigned short overrun;  // count of sampling time error
  uint32_t  timetag;  // time tag of the last sensor reading in micros
  unsigned char  data[504];
};

#endif
